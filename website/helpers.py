from datetime import datetime as dt
from .models import Petani, Pertanyaan, Jawaban, Bookmark, Vote
from flask_login import current_user


def get_date(date):
    now = dt.now()
    post_date = date
    diff = now - post_date
    if diff.days < 1:
        second = diff.seconds
        if second < 60:
            return f"{second} detik yang lalu"
        elif second < 3600:
            return f"{second//60} menit yang lalu"
        else:
            return f"{second//3600} jam yang lalu"
    else:
        return post_date.strftime("%d %b, %Y")


def get_user_from_id(id):
    return Petani.query.get(int(id))


def get_answer_from_id(id):
    return Jawaban.query.get(id)


def get_answer_count(post: Pertanyaan):
    return Jawaban.query.filter_by(id_pertanyaan=post.id).count()


def get_class(id, type):
    vote = Vote.query.filter_by(id_jawaban=id, id_petani=current_user.id).first()
    if type == "notif":
        print("notif")
        if not id:
            return "unread"
        else:
            return ""

    if type == "bookmark":
        bookmark = Bookmark.query.filter_by(id_pertanyaan=id, id_petani=current_user.id).first()
        if bookmark:
            return "bi-bookmark-fill"
        else:
            return "bi-bookmark"
    elif vote:
        thumb = "up" if vote.tipe == "like" else "down"
        if vote.tipe == type:
            return f"bi-hand-thumbs-{thumb}-fill"
        else:
            return f"bi-hand-thumbs-{'up' if type == 'like' else 'down'}"
    else:
        thumb = "up" if type == "like" else "down"
        return f"bi-hand-thumbs-{thumb}"


def get_judul_from_id(id):
    pertanyaan = Pertanyaan.query.get(id)
    return pertanyaan.judul
