from . import db

from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_ckeditor import CKEditorField


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
    id_petani = db.Column(db.Integer, db.ForeignKey("petani.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    judul = db.Column(db.String(255))
    detail = db.Column(db.Text)
    tags = db.Column(db.String(255))


class Jawaban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_pertanyaan = db.Column(db.Integer, db.ForeignKey("pertanyaan.id"))
    id_petani = db.Column(db.Integer, db.ForeignKey("petani.id"))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    detail = db.Column(db.Text)


class Gambar_pertanyaan(db.Model):
    id_pertanyaan = db.Column(db.Integer, db.ForeignKey("pertanyaan.id"), primary_key=True)
    gambar = db.Column(db.LargeBinary)


class Gambar_jawaban(db.Model):
    id_jawaban = db.Column(db.Integer, db.ForeignKey("jawaban.id"), primary_key=True)
    gambar = db.Column(db.LargeBinary)
