from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
    from .controller import controller

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(formHandle, url_prefix="/")
    app.register_blueprint(controller, url_prefix="/")

    from .helpers import get_user_from_id, get_date, get_answer_count, get_class, get_judul_from_id, get_answer_from_id
    from .models import Petani

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    helper_functions = {
        "get_user_from_id": get_user_from_id,
        "get_date": get_date,
        "get_answer_count": get_answer_count,
        "get_class": get_class,
        "get_judul_from_id": get_judul_from_id,
        "get_answer_from_id": get_answer_from_id,
    }

    for func_name, func in helper_functions.items():
        app.jinja_env.globals.update({func_name: func})

    @login_manager.user_loader
    def load_user(id):
        return Petani.query.get(int(id))

    return app
