from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Pertanyaan, Jawaban, Bookmark, Notifikasi, AnswerForm
from . import db
from datetime import datetime
import pytz

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template(
        "home.html",
        posts=Pertanyaan.query.order_by(Pertanyaan.date.desc()).all(),
    )


@views.errorhandler(405)
def all_exceptions(Exception):
    return render_template("errorPage.html"), 500


@views.route("/notification")
def notification():
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

    notifications = get_notifications(current_user.id)
    return render_template("notification.html", notifications=notifications)


@views.route("/forgotPassword")
def forgotPassword():
    return render_template("forgot-password.html")


@views.route("/pertanyaanku/<type>")
def pertanyaanku(type):
    if type == "asc":
        pertanyaan = Pertanyaan.query.filter_by(id_petani=current_user.id).order_by(Pertanyaan.date.asc())
    elif type == "desc":
        pertanyaan = Pertanyaan.query.filter_by(id_petani=current_user.id).order_by(Pertanyaan.date.desc())
    return render_template("pertanyaanku.html", my_posts=pertanyaan)


@views.route("/disimpan")
def disimpan():
    # Mendapatkan daftar id pertanyaan yang dibookmark oleh user
    id_pertanyaan_bookmarked = [bm.id_pertanyaan for bm in Bookmark.query.filter_by(id_petani=current_user.id)]

    # Menggunakan daftar id pertanyaan untuk memfilter data dari table "pertanyaan"
    pertanyaan_bookmarked = Pertanyaan.query.filter(Pertanyaan.id.in_(id_pertanyaan_bookmarked))

    return render_template("disimpan.html", posts=pertanyaan_bookmarked, user=current_user)


@views.route("/hapusProfil", methods=["GET", "POST"])
def hapusProfil():
    if request.method == "POST":
        db.session.delete(current_user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("hapusProfil.html", user=current_user)


@views.route("/jawaban/<type>")
def jawaban(type):
    if type == "desc":
        answers = Jawaban.query.filter_by(id_petani=current_user.id).order_by(Jawaban.date.desc())
    else:
        answers = Jawaban.query.filter_by(id_petani=current_user.id).order_by(Jawaban.date.asc())
    return render_template("jawaban.html", answers=answers)


@views.route("/detailPertanyaan/<id>", methods=["GET"])
def detailPertanyaan(id):
    form = AnswerForm(request.form)
    jawaban = Jawaban.query.filter_by(id_petani=current_user.id, id_pertanyaan=id).first()
    if jawaban:
        form.detail.data = jawaban.detail
    post = Pertanyaan.query.get(id)
    answers = Jawaban.query.filter_by(id_pertanyaan=id)
    return render_template("detailPertanyaan.html", post=post, form=form, answers=answers)


@views.route("/editJawaban/<id>", methods=["GET", "POST"])
def editJawaban(id):
    answer = Jawaban.query.filter_by(id_petani=current_user.id, id_pertanyaan=id).first()
    form = AnswerForm(request.form, obj=answer)
    if request.method == "POST":
        answer.detail = form.detail.data
        current_time = datetime.now(pytz.timezone("Asia/Jakarta"))
        answer.date = current_time
        db.session.commit()
    return redirect(url_for("views.detailPertanyaan", id=answer.id_pertanyaan))


@views.route("/tambahJawaban/<id>", methods=["POST"])
def tambahJawaban(id):
    form = AnswerForm(request.form)
    post = Pertanyaan.query.get(id)
    if request.method == "POST":
        detail = form.detail.data
        user_id = current_user.id
        current_time = datetime.now(pytz.timezone("Asia/Jakarta"))
        new_answer = Jawaban(id_pertanyaan=id, id_petani=user_id, detail=detail, date=current_time)
        db.session.add(new_answer)
        db.session.commit()
        if user_id != post.id_petani:
            notifikasi = Notifikasi(
                id_petani=post.id_petani, tipe="jawab", id_pertanyaan=id, id_jawaban=new_answer.id, date=current_time
            )
            db.session.add(notifikasi)
            db.session.commit()
        return redirect(url_for("views.detailPertanyaan", id=id))


@views.route("/searchPage/<key>")
def searchPage(key):
    pertanyaan = Pertanyaan.query.filter(Pertanyaan.judul.like("%" + key + "%"))
    return render_template("searchPage.html", posts=pertanyaan, key=key)
