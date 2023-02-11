from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Pertanyaan, Jawaban, Bookmark, Notifikasi, AnswerForm
from . import db

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template(
        "home.html",
        posts=Pertanyaan.query.order_by(Pertanyaan.date.desc()).all(),
    )


@views.route("/errorPage")
def errorPage():
    return render_template("errorPage.html")


@views.route("/notification")
def notification():
    notifications = Notifikasi.query.filter_by(
        id_petani=current_user.id).order_by(Notifikasi.date.desc())
    return render_template("notification.html", notifications=notifications)


@views.route("/forgotPassword")
def forgotPassword():
    return render_template("forgot-password.html")


@views.route("/pertanyaanku/<type>")
def pertanyaanku(type):
    if type == "asc":
        pertanyaan = Pertanyaan.query.filter_by(
            id_petani=current_user.id).order_by(Pertanyaan.date.asc())
    elif type == "desc":
        pertanyaan = Pertanyaan.query.filter_by(
            id_petani=current_user.id).order_by(Pertanyaan.date.desc())
    return render_template("pertanyaanku.html", my_posts=pertanyaan)


@views.route("/disimpan")
def disimpan():
    # Mendapatkan daftar id pertanyaan yang dibookmark oleh user
    id_pertanyaan_bookmarked = [
        bm.id_pertanyaan for bm in Bookmark.query.filter_by(id_petani=current_user.id)]

    # Menggunakan daftar id pertanyaan untuk memfilter data dari table "pertanyaan"
    pertanyaan_bookmarked = Pertanyaan.query.filter(
        Pertanyaan.id.in_(id_pertanyaan_bookmarked))

    return render_template("disimpan.html", posts=pertanyaan_bookmarked, user=current_user)


@views.route("/hapusProfil", methods=["GET", "POST"])
def hapusProfil():
    if request.method == "POST":
        db.session.delete(current_user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("hapusProfil.html", user=current_user)


@views.route("/jawaban")
def jawaban():
    answers = Jawaban.query.filter_by(id_petani=current_user.id)
    return render_template("jawaban.html", answers=answers)


@views.route("/detailPertanyaan/<id>", methods=["GET"])
def detailPertanyaan(id):
    form = AnswerForm(request.form)
    jawaban = Jawaban.query.filter_by(
        id_petani=current_user.id, id_pertanyaan=id).first()
    if jawaban:
        form.detail.data = jawaban.detail
    post = Pertanyaan.query.get(id)
    answers = Jawaban.query.filter_by(id_pertanyaan=id)
    return render_template("detailPertanyaan.html", post=post, form=form, answers=answers)


@views.route("/editJawaban/<id>", methods=["GET", "POST"])
def editJawaban(id):
    answer = Jawaban.query.filter_by(
        id_petani=current_user.id, id_pertanyaan=id).first()
    form = AnswerForm(request.form, obj=answer)
    if request.method == "POST":
        answer.detail = form.detail.data
        db.session.commit()
    return redirect(url_for("views.detailPertanyaan", id=answer.id_pertanyaan))


@views.route("/tambahJawaban/<id>", methods=["POST"])
def tambahJawaban(id):
    form = AnswerForm(request.form)
    post = Pertanyaan.query.get(id)
    if request.method == "POST":
        detail = form.detail.data
        user_id = current_user.id
        new_answer = Jawaban(
            id_pertanyaan=id, id_petani=user_id, detail=detail)
        db.session.add(new_answer)
        db.session.commit()
        notifikasi = Notifikasi(
            id_petani=post.id_petani,
            tipe="jawab",
            id_pertanyaan=id,
            id_jawaban=new_answer.id,
        )
        db.session.add(notifikasi)
        db.session.commit()
        return redirect(url_for("views.detailPertanyaan", id=id))


@views.route("/searchPage")
def searchPage():
    return render_template(
        "searchPage.html",
        posts=Pertanyaan.query.order_by(Pertanyaan.date.desc()).all(),
    )
