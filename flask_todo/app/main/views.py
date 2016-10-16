# coding:utf-8
from . import main
from flask import render_template, redirect, url_for, request
from flask_babel import gettext as _
from forms import ThingForm, EditForm, DeleteForm
from app.models import Role, User, State, Thing
from app import db
from flask_login import login_required, current_user


@main.route('/', methods=['GET', 'POST'])
def index():
    thing_form = ThingForm()
    if thing_form.validate_on_submit():
        author = current_user._get_current_object()
        thing_add = Thing(thing=thing_form.thing.data, author=author, status_id=2)
        db.session.add(thing_add)
        db.session.commit()
        return redirect(url_for('main.todo', id=thing_add.author_id))
    return render_template('index.html', title=_('Welcome to To Do List Web'), thing_form=thing_form)


@main.route('/todo/<int:id>', methods=['GET', 'POST'])
@login_required
def todo(id):
    page_index = request.args.get('page', 1, type=int)
    query = Thing.query.filter_by(author_id=id).order_by(Thing.id.desc())
    pagination = query.paginate(page_index, per_page=6, error_out=False)
    post_index = pagination.items

    thing_form = ThingForm()
    if thing_form.validate_on_submit():
        thing_add = Thing(thing=thing_form.thing.data, author_id=id, status_id=2)
        db.session.add(thing_add)
        db.session.commit()
        return redirect(url_for('main.todo', id=id))

    edit_form = EditForm()
    delete_form =DeleteForm()
    title = _('Things To Do')

    return render_template('todo.html', todolist=post_index,
                           thing_form=thing_form, edit_form=edit_form,
                           delete_form=delete_form, title=title,
                           pagination=pagination,
                           )


@main.route('/completed/<int:id>', methods=['GET', 'POST'])
@login_required
def completed(id):
    page_index = request.args.get('page', 1, type=int)
    query = Thing.query.filter_by(author_id=id).order_by(Thing.id.desc())
    pagination = query.paginate(page_index, per_page=6, error_out=False)
    post_index = pagination.items

    thing_form = ThingForm()
    if thing_form.validate_on_submit():
        thing_add = Thing(thing=thing_form.thing.data, author_id=id, status_id=2)
        db.session.add(thing_add)
        db.session.commit()
        return redirect(url_for('main.todo', id=id))

    edit_form = EditForm()
    delete_form =DeleteForm()
    title = _('Things Completed')

    return render_template('completed.html', todolist=post_index,
                           thing_form=thing_form, edit_form=edit_form,
                           delete_form=delete_form, title=title,
                           pagination=pagination,
                           )


@main.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        edit_id = request.form['id']
        edit_thing = request.form['thing']
        edit_model = Thing.query.get_or_404(edit_id)
        edit_model.thing = edit_thing
        db.session.add(edit_model)
        db.session.commit()
        return render_template('demo.html')
    return render_template('demo.html')


@main.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        delete_id = request.form['delete_id']
        edit_model = Thing.query.get_or_404(delete_id)
        db.session.delete(edit_model)
        db.session.commit()
        return render_template('demo.html')
    return render_template('demo.html')


@main.route('/complete', methods=['GET', 'POST'])
@login_required
def complete():
    if request.method == 'POST':
        complete_status_id = request.form['check_input']
        complete_id = request.form['check_thing']
        complete_model = Thing.query.get_or_404(complete_id)
        complete_model.status_id = complete_status_id
        db.session.add(complete_model)
        db.session.commit()
        return render_template('demo.html')
    return render_template('demo.html')


