# coding:utf-8
from flask import render_template, redirect, request
from flask_nav import Nav
from flask_nav.elements import *
from . import main
from flask_babel import Babel, gettext as _

# nav = Nav(main)
# nav.register_element('top', Navbar(u'Flask入门', View(u'主页', 'index'),
#                                    View(u'模板', 'base'),
#                                    View(u'小测试', 'home' ),
#                                    View(u'模板', 'project'),
#                                    View(u'登录', 'login'),
#                                    View(u'上传', 'upload'),
#                                    View(u'cookie', 'cookie'),
#                                    ))


@main.route('/')
def index():
    # post_index = Post.query.all()
    page_index = request.args.get('page', 1, type=int)
    query = Post.query.order_by(Post.created.desc())
    pagination = query.paginate(page_index, per_page=10, error_out=False)
    post_index = pagination.items
    title = _(u'flask博客世界')
    # if current_user.is_authenticated:
    #     title = current_user.name + u'的博客'
    return render_template('index.html', title=title, posts=post_index, pagination=pagination)


# 装饰器装饰vies function, 定义路由路径
# hello_world向浏览器输出内容的函数
@main.route('/home')
def home():
    return 'HAVE you! a good boy'


@main.route('/about')
@main.route('/about2')
def about():
    return 'this is a url_for'

# about有文件名性质，url后面不能加斜杠/，例如http://127.0.0.1:5000/about


@main.route('/project/')
def project():
    return 'this is a project for flask'
# project有目录性质，整个函数类似指向project目录下默认的文件例如default, index.html等，
# 文件名后面可以加斜杠127.0.0.1:5000/project/


# 设置参数后，必须有参数传入，不然会出现400错误
# request 引用自flask库，测试http方法
@main.route('/upload', methods=['GET', 'POST'])
def upload():
    from flask import redirect, url_for
    from werkzeug.utils import secure_filename
    from os import path
    if request.method == 'POST':
        _file = request.files['file']
        base_path = path.abspath(path.dirname(__file__))
        upload_path = path.join(base_path, 'static\uploads', secure_filename(_file.filename))
        # 在这里要特别注意，构成的完整路径应该同时包含上传文件的文件名
        try:
            _file.save(upload_path)
        except Exception, e:
            print e
        return redirect(url_for('upload'))
    return render_template('upload.html')


@main.route('/cookie')
def cookie():
    from flask import make_response
    response = make_response(render_template('index.html', title='cookie1'))
    response.set_cookie('username', 'liming')
    return response


@main.route('/base')
def base():
    return render_template('base.html')


@main.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

#  ========================================================from
from ..models import Post, Comment
from forms import CommentForm, PostForm
from .. import db
from flask_login import login_required, current_user
import time


@main.route('/posts/<int:id>', methods=['GET', 'POST'])
def posts(id):
    # 查询Post表的这个作者的详情
    post = Post.query.get_or_404(id)
    form = CommentForm()
    title = post.title
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, authors=current_user._get_current_object(), post_id=id)
        db.session.add(comment)
        try:
            db.session.commit()
        except:
            db.session.rollback()

    return render_template('posts/detail.html', post=post, form=form, title=title)


# @main.route('/edit', methods=['GET', 'POST'])
# @main.route('/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit(id=0):
#     form = PostForm()
#
#     if form.validate_on_submit():
#         post.title = form.title.data
#         post.body = form.body.data
#         db.session.add(post)
#         try:
#             db.session.commit()
#         except:
#             db.session.rollback()
#
#         return render_template(url_for('post'), id=post.id)
#
#     title = u'添加新文章'
#     return render_template('posts/edit.html', post=post, form=form, title=title)




@main.route('/edit', methods=['GET', 'POST'])
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id=0):
    form = PostForm()

    if id == 0:
        post = Post()
    else:
        post = Post.query.get_or_404(id)

    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.author = current_user._get_current_object()
        db.session.add(post)
        try:
            db.session.commit()
        except:
            db.session.rollback()

        time.sleep(1)
        return redirect(url_for('main.posts', id=post.id))
    # 在这里用redirect，不能用render_template

    form.title.data = post.title
    form.body.data = post.body

    title = _(u'添加新文章')
    if id > 0:
        title = _(u'编辑文章') + '-' + _(post.title)

    return render_template('posts/edit.html', post=post, form=form, title=title)






