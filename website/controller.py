from flask import Blueprint, request, jsonify, url_for, redirect
from flask_login import login_required, current_user
from .models import Bookmark, Jawaban, Vote, Notifikasi, Pertanyaan
from . import db
from datetime import datetime
import pytz

controller = Blueprint("controller", __name__)


@controller.route("/api/bookmark", methods=["POST", "DELETE"])
@login_required
def bookmark():
    if request.method == "POST":
        post_id = request.form.get("post_id")
        bookmark = Bookmark.query.filter_by(id_pertanyaan=post_id, id_petani=current_user.id).first()
        if not bookmark:
            # jika belum, tambahkan ke database
            bookmark = Bookmark(id_pertanyaan=post_id, id_petani=current_user.id)

            db.session.add(bookmark)
        else:
            db.session.delete(bookmark)
        db.session.commit()
        return "nice"


@controller.route("/remove/<id>")
def remove(id):
    pertanyaan = Pertanyaan.query.get(id)
    db.session.delete(pertanyaan)
    db.session.commit()
    return redirect(url_for("views.home"))


@controller.route("/removeAnswer/<id>")
def removeAnswer(id):
    jawaban = Jawaban.query.get(id)
    post_id = jawaban.id_pertanyaan
    db.session.delete(jawaban)
    db.session.commit()
    return redirect(url_for("views.detailPertanyaan", id=post_id))


@controller.route("/api/jawaban/like_dislike", methods=["POST"])
@login_required
def like_dislike_jawaban():
    jawaban_id = request.form.get("jawaban_id")
    tipe = request.form.get("tipe")
    petani_id = current_user.id
    jawaban = Jawaban.query.get(jawaban_id)
    # Mengecek apakah petani sudah memberikan vote pada jawaban ini
    vote = Vote.query.filter_by(id_petani=petani_id, id_jawaban=jawaban_id).first()
    if vote:
        # Jika petani sudah memberikan vote
        notifikasi = Notifikasi.query.filter_by(
            id_petani=petani_id,
            id_pertanyaan=jawaban.id_pertanyaan,
            id_jawaban=jawaban.id,
        ).first()
        if vote.tipe == tipe:
            # Jika tipe vote sebelumnya sama dengan tipe yang dipilih sekarang, maka hapus vote
            if tipe == "like":
                jawaban.likes -= 1
                if current_user.id != jawaban.id_petani:
                    db.session.delete(notifikasi)
            else:
                jawaban.dislikes -= 1
            db.session.delete(vote)
        else:
            # Jika tipe vote sebelumnya berbeda dengan tipe yang dipilih sekarang, maka ubah vote
            if tipe == "like":
                jawaban.likes += 1
                jawaban.dislikes -= 1
                current_time = datetime.now(pytz.timezone("Asia/Jakarta"))
                notifikasi = Notifikasi(
                    id_petani=petani_id,
                    tipe=tipe,
                    id_pertanyaan=jawaban.id_pertanyaan,
                    id_jawaban=jawaban.id,
                    date=current_time,
                )
                if current_user.id != jawaban.id_petani:
                    db.session.add(notifikasi)
            else:
                jawaban.dislikes += 1
                jawaban.likes -= 1
                if current_user.id != jawaban.id_petani:
                    db.session.delete(notifikasi)
            vote.tipe = tipe
    else:
        # Jika petani belum memberikan vote, maka buat vote baru
        current_time = datetime.now(pytz.timezone("Asia/Jakarta"))
        vote = Vote(id_petani=petani_id, id_jawaban=jawaban_id, tipe=tipe, date=current_time)
        if tipe == "like":
            jawaban.likes += 1
            notifikasi = Notifikasi(
                id_petani=current_user.id,
                tipe=tipe,
                id_pertanyaan=jawaban.id_pertanyaan,
                id_jawaban=jawaban.id,
                date=current_time,
            )
            if current_user.id != jawaban.id_petani:
                db.session.add(notifikasi)
        else:
            jawaban.dislikes += 1
        db.session.add(vote)
    db.session.commit()
    return jsonify({"status": "success"})


@controller.route("/api/jawaban/like_dislike_count", methods=["GET"])
def like_dislike_count():
    jawaban_id = request.args.get("jawaban_id")
    jawaban = Jawaban.query.get(jawaban_id)
    like = jawaban.likes
    dislike = jawaban.dislikes
    return jsonify({"like": like, "dislike": dislike})


@controller.route("api/bookmark/count", methods=["GET"])
def count_disimpan():
    id_petani = current_user.id
    count = Bookmark.query.filter_by(id_petani=id_petani).count()
    return str(count)


@controller.route("/api/notif", methods=["POST"])
def api_notif():
    notif_id = request.form.get("notif_id")
    if notif_id == "all":

        def get_notifications(current_user_id):
            notifications = (
                Notifikasi.query.join(Pertanyaan, Notifikasi.id_pertanyaan == Pertanyaan.id)
                .filter(Pertanyaan.id_petani == current_user_id)
                .union(
                    Notifikasi.query.join(Jawaban, Notifikasi.id_jawaban == Jawaban.id)
                    .filter(Jawaban.id_petani == current_user_id)
                    .filter(Notifikasi.tipe == "like")
                )
                .order_by(Notifikasi.date.desc())
            )
            return notifications

        notifs = get_notifications(current_user.id)
        for notif in notifs:
            notif.dibaca = True
        db.session.commit()
        return "success"
    else:
        notif = Notifikasi.query.get(notif_id)
        notif.dibaca = True
        db.session.commit()
        return jsonify({"redirect_url": url_for("views.detailPertanyaan", id=notif.id_pertanyaan)})


@controller.route("/api/search", methods=["GET"])
def search():
    query = request.args.get("query")
    print(query)
    pertanyaan = Pertanyaan.query.filter(Pertanyaan.judul.like("%" + query + "%")).all()
    result = []
    for p in pertanyaan:
        result.append({"id": p.id, "judul": p.judul})
    return jsonify(result)
