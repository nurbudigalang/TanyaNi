from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
@login_required
def home():
    return render_template("home.html")


@views.route("/errorPage")
def errorPage():
    return render_template("errorPage.html")


@views.route("/notification")
def notification():
    return render_template("notification.html")


@views.route("/buatPertanyaan")
def buatPertanyaan():
    return render_template("buatPertanyaan.html")


@views.route("/forgotPassword")
def forgotPassword():
    return render_template("forgot-password.html")


@views.route("/pertanyaanku")
def pertanyaanku():
    return render_template("pertanyaanku.html")
