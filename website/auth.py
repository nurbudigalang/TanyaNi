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
                flash("Anda Berhasil Login!", category="success")
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

        if password1 != password2:
            flash("Password tidak sesuai", category="error")
            pass
        elif len(password1) < 8:
            flash("Panjang password minimal 8 Character", category="error")
            pass
        elif len(nama) < 3:
            flash("panjang nama minimal 3 character", category="error")
            pass
        else:
            # kondisi terpenuhi untuk membuat akun
            petani_baru = Petani(nama=nama, email=email, password=generate_password_hash(password1, method="sha256"))
            db.session.add(petani_baru)
            db.session.commit()
            login_user(petani_baru, remember=True)
            flash("Akun anda berhasil dibuat!", category="success")
            return redirect(url_for("views.home"))

    return render_template("create-account.html", user=current_user)
