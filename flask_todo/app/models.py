# coding:utf-8
from flask_login import UserMixin
from app import login_manager, db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    users = db.relationship('User', backref='roles')    # 表映射1，主表关联附属表,backref 映射关系的名称，映射关系在另外一个表自动生成

    @staticmethod
    def role_seed():
        db.session.add_all(map(lambda r: Role(name=r), ['Guests', 'Administrators']))
        db.session.commit()


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)
    roles_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    things = db.relationship('Thing', backref='author')

    @staticmethod
    def on_created(target, value, oldvalue, initiator):
        target.roles = Role.query.filter_by(name='Guests').first()

db.event.listen(User.name, 'set', User.on_created)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String)

    things = db.relationship('Thing', backref='status')

    @staticmethod
    def state_seed():
        db.session.add_all(map(lambda r: State(state=r), ['Complete', 'To do']))
        db.session.commit()


class Thing(db.Model):
    __tablename__ = 'things'
    id = db.Column(db.Integer, primary_key=True)
    thing = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('states.id'))
