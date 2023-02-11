from flask import Blueprint, render_template, request, url_for, send_from_directory, make_response, redirect
from os.path import join, dirname, realpath
from flask_login import current_user
from .models import Pertanyaan, PostForm
from . import db
from datetime import datetime
import pytz

formHandle = Blueprint("formHandle", __name__)


@formHandle.route("files/<path:filename>")
def upload_files(filename):
    path = join(dirname(realpath(__file__)), "static/upload/")
    return send_from_directory(path, filename)


@formHandle.route("/buatPertanyaan", methods=["GET", "POST"])
def buatPertanyaan():
    form = PostForm(request.form)
    if request.method == "POST":
        judul = form.judul.data
        detail = form.detail.data
        user_id = current_user.id
        current_time = datetime.now(pytz.timezone("Asia/Jakarta"))
        new_post = Pertanyaan(id_petani=user_id, judul=judul, detail=detail, date=current_time)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("views.detailPertanyaan", id=new_post.id))

    return render_template("buatPertanyaan.html", form=form)


@formHandle.route("editPertanyaan/<id>", methods=["GET", "POST"])
def editPertanyaan(id):
    pertanyaan = Pertanyaan.query.get(id)
    form = PostForm(request.form, obj=pertanyaan)
    if request.method == "POST":
        pertanyaan.judul = form.judul.data
        current_time = datetime.now(pytz.timezone("Asia/Jakarta"))
        pertanyaan.date = current_time
        print(pertanyaan.judul)
        pertanyaan.detail = form.detail.data
        db.session.commit()
        return redirect(url_for("views.detailPertanyaan", id=pertanyaan.id))
    return render_template("editPertanyaan.html", form=form, post=pertanyaan)


@formHandle.route("/upload", methods=["POST"])
def upload():
    callback = request.args.get("CKEditorFuncNum")
    error = ""
    f = request.files.get("upload")
    extension = f.filename.split(".")[-1].lower()
    if extension not in ["jpg", "png", "gif", "jpeg"]:
        error = "Hanya dapat berisi Gambar !"

    f.save(join(dirname(realpath(__file__)), "static/upload/", f.filename))
    url = url_for("static", filename="%s/%s" % ("upload", f.filename))
    res = """<script type="text/javascript"> 
             window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
             </script>""" % (
        callback,
        url,
        error,
    )
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response
