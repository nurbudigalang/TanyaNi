from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Petani
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        petani = Petani.query.filter_by(email=email).first()
        if petani is not None:
            if check_password_hash(petani.password, password):
                login_user(petani, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password Salah!", category="error")
        else:
            flash("Akun belum terdaftar, silahkan sign Up dahulu!", category="error")
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/createAccount", methods=["GET", "POST"])
def createAccount():
    if request.method == "POST":
        nama = request.form.get("nama")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        valid, message = validate_account(nama, email, password1, password2)

        if valid:
            petani_baru = create_new_account(nama, email, password1)
            login_user(petani_baru, remember=True)
            return redirect(url_for("views.home"))
        else:
            flash(message, category="error")

    return render_template("create-account.html", user=current_user)


def validate_account(nama, email, password1, password2):
    if password1 != password2:
        return False, "Password tidak sesuai"
    elif len(password1) < 8:
        return False, "Panjang password minimal 8 Character"
    elif len(nama) < 3:
        return False, "panjang nama minimal 3 character"
    elif Petani.query.filter_by(email=email).first() is not None:
        return False, "Email sudah terdaftar!"
    else:
        return True, ""


def create_new_account(nama, email, password):
    petani_baru = Petani(nama=nama, email=email, password=generate_password_hash(password, method="sha256"))
    db.session.add(petani_baru)
    db.session.commit()
    return petani_baru


@auth.route("/editProfil", methods=["POST", "GET"])
def editProfil():
    if request.method == "POST":
        nama = request.form.get("nama")
        lokasi = request.form.get("lokasi")
        pekerjaan = request.form.get("pekerjaan")
        tentang_saya = request.form.get("tentang_saya")

        if len(nama) <= 3:
            flash("Nama harus lebih dari 3 Karakter")
        elif len(lokasi) <= 3:
            flash("Lokasi harus lebih dari 3 Karakter")
        elif len(pekerjaan) <= 3:
            flash("Lokasi harus lebih dari 3 Karakter")
        else:
            current_user.nama = nama
            current_user.lokasi = lokasi
            current_user.pekerjaan = pekerjaan
            current_user.tentang_saya = tentang_saya
            db.session.commit()
    return render_template("editProfil.html", user=current_user)
