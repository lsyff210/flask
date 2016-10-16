# coding:utf-8
from os import path

from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_nav import Nav
from flask_nav.elements import *
from flask_login import LoginManager, current_user
from flask_pagedown import PageDown
from flask_gravatar import Gravatar
from flask_babel import Babel, gettext as _
from config import config

babel = Babel()
nav = Nav()   # nav1 可以转移到views.py init_views()函数下，转以后为nav = Nav(app)
bootstrap = Bootstrap()

# 数据库链接
# base_dir = path.abspath(path.dirname(__file__))   # 转移到config.py设置中
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'author.login'
# 指定login页面


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 转移到config.py设置中
    # app.config.from_pyfile('config')  # app.secret_key = 'hard to guess string'具有替代作用
    # app.secret_key = 'hard to guess string'
    # app.config['BABEL_DEFAULT_LOCALE'] = 'zh'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + path.join(base_dir, 'data.sqlite')
    # app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    # app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)


    # 实例化蓝图blueprint
    from author import author as author_blueprint
    from main import main as main_blueprint
    app.register_blueprint(author_blueprint, url_prefix='/author')
    app.register_blueprint(main_blueprint)

    # nav1 可以转移到views.py init_views()函数下
    nav.register_element('top', Navbar(_(u'Flask入门'), View(_(u'主页'), 'main.index'),
                                       View(_(u'模板'), 'main.base'),
                                       View(_(u'小测试'), 'main.home' ),
                                       View(_(u'模板'), 'main.project'),
                                       View(_(u'登录'), 'author.login'),
                                       View(_(u'注册'), 'author.register'),
                                       View(_(u'上传'), 'main.upload'),
                                       View(_(u'cookie'), 'main.cookie'),
                                       ))
    nav.init_app(app)      # nav1 可以转移到views.py init_views()函数下,转以后删除
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)  # login_manager1 实例化login_manager
    pagedown.init_app(app)
    Gravatar(app, 64)
    babel.init_app(app)

    # 自己构造jinjia  Builtin Filters
    @app.template_test('current_link')
    def is_current_link(link):
        return link == request.path

    # @babel.localeselector
    # def get_locale():
    #     return current_user.locale
    # # 获取用户所在地区，只有在models用户表中设置了locale之后才会起作用
    #
    # @babel.timezoneselector
    # def get_timezone():
    #     return current_user.timezone    # zh +8
    #  # 获取用户所在时区，只有在models用户表中设置了timezone之后才会起作用

    # @babel.localeselector
    # def get_locale():
    #     return current_user.locale

    return app








