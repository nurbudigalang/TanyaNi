from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_ckeditor import CKEditor

db = SQLAlchemy()
DB_NAME = "tanyaNi.db"
ckeditor = CKEditor()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "lancarkanlah project kami ya Tuhan"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["CKEDITOR_FILE_UPLOADER"] = "formHandle.upload"
    app.config["CKEDITOR_HEIGHT"] = 500
    ckeditor.init_app(app)
    db.init_app(app)
    from .views import views
    from .auth import auth
    from .formHandle import formHandle

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(formHandle, url_prefix="/")

    from .models import Petani, Pertanyaan, Jawaban, Gambar_jawaban, Gambar_pertanyaan

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Petani.query.get(int(id))

    return app
