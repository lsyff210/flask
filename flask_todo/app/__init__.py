# coding:utf-8
from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from config import config
from flask_babel import Babel
from flask_wtf import CsrfProtect


babel = Babel()  # 全球化
bootstrap = Bootstrap()   # 模板继承和装饰
db = SQLAlchemy()  # 数据库
crsf = CsrfProtect()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'author.login'
# 指定login页面


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    babel.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    crsf.init_app(app)

    from author import author as author_blueprint
    from main import main as main_blueprint
    app.register_blueprint(author_blueprint, url_prefix='/author')
    app.register_blueprint(main_blueprint)

    return app
