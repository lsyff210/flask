# coding:utf-8
from . import db
from app import login_manager
from flask_login import UserMixin
# from flask_login import AnonymousUserMixin匿名用户的定制处理
import datetime
from markdown import markdown

class Role(db.Model):   # 创建实体变量，数据库中的表
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    users = db.relationship('User', backref='roles')    # 表映射1，主表关联附属表,backref 映射关系的名称，映射关系在另外一个表自动生成

    @staticmethod
    def seed():
        db.session.add_all(map(lambda r: Role(name=r), ['Guests', 'Administrators']))
        db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    name = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 表映射1，主表关联附属表

    post = db.relationship('Post', backref='author')
    comments = db.relationship('Comment', backref='authors')

    @staticmethod
    def on_created(target, value, oldvalue, initiator):
        target.roles = Role.query.filter_by(name='Guests').first()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# 当用户成功登录后，返回cookie

db.event.listen(User.name, 'set', User.on_created)



class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    body = db.Column(db.String)
    body_html = db.Column(db.String)
    created = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    comments = db.relationship('Comment', backref='post')

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        if value is None or value is '':
            target.body_html = ''
        else:
            target.body_html = markdown(value)

db.event.listen(Post.body, 'set', Post.on_body_changed)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    created = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    authors_id = db.Column(db.Integer, db.ForeignKey('users.id'))






