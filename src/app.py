import logging
import os

from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()


def __db_setup(_app, _app_setting, db_pg: bool = False):
    if db_pg:
        _app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost:5432/app_base"
        _app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_size': 10, 'max_overflow': 20}
    else:
        _app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{_app_setting.data_dir}/data.db?timeout=60'
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _app.config['SQLALCHEMY_ECHO'] = False
    return _app


def create_app(app_setting) -> Flask:
    os.environ.setdefault('FLASK_ENV', 'production' if app_setting.prod else 'development')
    app = Flask(__name__)
    cors = CORS()
    app_setting = app_setting.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors.init_app(app)
    db.init_app(__db_setup(app, app_setting))

    def setup(self):
        gunicorn_logger = logging.getLogger('gunicorn.error')
        self.logger.handlers = gunicorn_logger.handlers
        self.logger.setLevel(gunicorn_logger.level)
        self.logger.info(self.config['SQLALCHEMY_DATABASE_URI'])

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    @app.before_first_request
    def create_default_user():
        import uuid as uuid_
        from src.models.user.model_user import UserModel
        from src.models.enum import RoleType, StateType
        from src.resources.utils import encrypt_password
        user = UserModel.find_by_username('admin')
        if not user:
            uuid = str(uuid_.uuid4())
            user = UserModel(uuid=uuid, username="admin", password="N00BWires", email="admin@nubeio.com",
                             role=RoleType.ADMIN, state=StateType.VERIFIED)
            user.password = encrypt_password(user.password)
            user.save_to_db()

    @app.before_request
    def before_request_fn():
        env: dict = request.environ
        if not (env.get('REMOTE_ADDR', '') == "127.0.0.1" and "python-requests" in env.get('HTTP_USER_AGENT', '')):
            from src.resources.utils import authorize
            authorize()

    def register_router(_app) -> Flask:
        from src.routes import bp_system, bp_users, bp_devices
        _app.register_blueprint(bp_system)
        _app.register_blueprint(bp_users)
        _app.register_blueprint(bp_devices)
        return _app

    setup(app)
    return register_router(app)
