from . import db
import pytz
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_ckeditor import CKEditorField
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import os

SQLALCHEMY_DB_URL = os.getenv("DB_CONN")


class Petani(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    lokasi = db.Column(db.String(255))
    pekerjaan = db.Column(db.String(255))
    tentang_saya = db.Column(db.Text)


class Pertanyaan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_petani = db.Column(
        db.Integer,
        db.ForeignKey("petani.id", ondelete="CASCADE"),
    )
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone("Asia/Jakarta")))
    judul = db.Column(db.String(255))
    detail = db.Column(db.Text)


class Jawaban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_pertanyaan = db.Column(
        db.Integer,
        db.ForeignKey("pertanyaan.id", ondelete="CASCADE"),
    )
    id_petani = db.Column(
        db.Integer,
        db.ForeignKey("petani.id", ondelete="CASCADE"),
    )
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone("Asia/Jakarta")))
    detail = db.Column(db.Text)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)


class Notifikasi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_petani = db.Column(
        db.Integer,
        db.ForeignKey("petani.id", ondelete="CASCADE"),
    )
    tipe = db.Column(db.String(255))
    id_pertanyaan = db.Column(
        db.Integer,
        db.ForeignKey("pertanyaan.id", ondelete="CASCADE"),
    )
    id_jawaban = db.Column(
        db.Integer,
        db.ForeignKey("jawaban.id", ondelete="CASCADE"),
    )
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone("Asia/Jakarta")))
    dibaca = db.Column(db.Boolean, default=False)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_petani = db.Column(
        db.Integer,
        db.ForeignKey("petani.id", ondelete="CASCADE"),
    )
    id_pertanyaan = db.Column(
        db.Integer,
        db.ForeignKey("pertanyaan.id", ondelete="CASCADE"),
    )
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone("Asia/Jakarta")))


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_petani = db.Column(
        db.Integer,
        db.ForeignKey("petani.id", ondelete="CASCADE"),
    )
    id_jawaban = db.Column(
        db.Integer,
        db.ForeignKey("jawaban.id", ondelete="CASCADE"),
    )
    tipe = db.Column(db.String(255))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now(pytz.timezone("Asia/Jakarta")))


# Helpers CLass
class AnswerForm(FlaskForm):
    detail = CKEditorField("detail")
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    judul = StringField("judul")
    detail = CKEditorField("detail")
    submit = SubmitField("Submit")
