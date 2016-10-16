# coding:utf-8
from flask import flash, render_template, redirect, url_for
from . import author
from forms import LoginForm, RegistrationForm
from ..models import *
from app import db
from flask_login import login_user, logout_user, current_user
from flask_babel import gettext as _


@author.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data, password=form.password.data).first()
        if user is not None:
            login_user(user)
            id = user.id
            return redirect(url_for('main.todo', id=id))
    return render_template('login.html', title=_(u'login'), form=form)


@author.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('author.login'))


@author.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    name=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('author.login'))

    return render_template('register.html',
                           title=_('register'),
                           form=form)