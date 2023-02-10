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


@views.route("/pertanyaanku")
def pertanyaanku():
    my_posts = Pertanyaan.query.filter_by(id_petani=current_user.id)
    return render_template("pertanyaanku.html", my_posts=my_posts)


@views.route("/disimpan")
def disimpan():
    # Mendapatkan daftar id pertanyaan yang dibookmark oleh user
    id_pertanyaan_bookmarked = [
        bm.id_pertanyaan for bm in Bookmark.query.filter_by(id_petani=current_user.id)]

    # Menggunakan daftar id pertanyaan untuk memfilter data dari table "pertanyaan"
    pertanyaan_bookmarked = Pertanyaan.query.filter(
        Pertanyaan.id.in_(id_pertanyaan_bookmarked))

    return render_template("disimpan.html", posts=pertanyaan_bookmarked, user=current_user)


@views.route("/hapusProfil")
def hapusProfil():
    return render_template("hapusProfil.html")


@views.route("/jawaban")
def jawaban():
    answers = Jawaban.query.filter_by(id_petani=current_user.id)
    return render_template("jawaban.html", answers=answers)


@views.route("/detailPertanyaan/<id>", methods=["GET", "POST"])
def detailPertanyaan(id):
    form = AnswerForm(request.form)
    post = Pertanyaan.query.get(id)
    answers = Jawaban.query.filter_by(id_pertanyaan=id)
    if request.method == "POST":
        detail = form.detail.data
        user_id = current_user.id
        new_answer = Jawaban(
            id_pertanyaan=id, id_petani=user_id, detail=detail)
        db.session.add(new_answer)
        db.session.commit()
        answers = Jawaban.query.filter_by(id_pertanyaan=id)
        notifikasi = Notifikasi(
            id_petani=post.id_petani,
            tipe="jawab",
            id_pertanyaan=id,
            id_jawaban=new_answer.id,
        )
        db.session.add(notifikasi)
        db.session.commit()
        return redirect(url_for("views.detailPertanyaan", id=id))
    return render_template("detailPertanyaan.html", post=post, form=form, answers=answers)


@views.route("/searchPage")
def searchPage():
    return render_template(
        "searchPage.html",
        posts=Pertanyaan.query.order_by(Pertanyaan.date.desc()).all(),
    )
