from . import db

from flask_login import UserMixin
from sqlalchemy.sql import func

class Petani(db.Model,UserMixin):
    id_petani = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    lokasi = db.Column(db.String(255))
    pekerjaan = db.Column(db.String(255))
    tentang_saya = db.Column(db.Text)

class Pertanyaan(db.Model):
    id_pertanyaan = db.Column(db.Integer, primary_key=True)
    id_petani = db.Column(db.Integer, db.ForeignKey('petani.id_petani'))
    date = db.Column(db.Datetime(timezone=True),default=func.now())
    judul = db.Column(db.String(255))
    detail = db.Column(db.Text)
    tags = db.Column(db.String(255))

class Jawaban(db.Model):
    id_jawaban = db.Column(db.Integer, primary_key=True)
    id_pertanyaan = db.Column(db.Integer, db.ForeignKey('pertanyaan.id_pertanyaan'))
    id_petani = db.Column(db.Integer, db.ForeignKey('petani.id_petani'))
    date = db.Column(db.Datetime(timezone=True),default=func.now())
    detail = db.Column(db.Text)


class Gambar_pertanyaan(db.Model):
    id_pertanyaan = db.Column(db.Integer,db.ForeignKey('pertanyaan.id_pertanyaan'), primary_key=True)
    gambar = db.Column(db.LargeBinary)

class Gambar_jawaban(db.Model):
    id_jawaban = db.Column(db.Integer,db.ForeignKey('pertanyaan.id_jawaban'), primary_key=True)
    gambar = db.Column(db.LargeBinary)
