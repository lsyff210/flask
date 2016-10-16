 # coding:utf-8
from app import create_app
# from flask.ext.script import Manager, Server
from flask_script import Manager, Server, Shell
import os
from app.models import Role, User, Post, Comment
from app import db


app = create_app()
# 使用扩展包启动，script包
manager = Manager(app)
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post, Comment=Comment)

manager.add_command('runserver',
                    # Shell(make_context=make_shell_context),
                    Server(use_debugger=True,
                           use_reloader=True,
                           port=5501,
                           extra_files=[os.path.join(app.root_path, app.template_folder),
                                        os.path.join(app.root_path, app.template_folder, 'includes'),
                                        os.path.join(app.root_path, app.template_folder, 'posts')
                                        ]
                           )
                    )
# 自动加载代码更新到视图窗口（网页前端）

from flask_migrate import Migrate, MigrateCommand, upgrade
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    from app.models import Role
    upgrade()
    Role.seed()


@manager.command
def forgerd():
    from forgery_py import internet, lorem_ipsum, date,basic
    from random import randint
    from app.models import Role, User, Post, Comment

    db.drop_all()
    db.create_all()
    Role.seed()
    guests = Role.query.first()

    def generate_user():
        return User(
            email=internet.email_address(),
            name=internet.user_name(),
            password=basic.text(6, at_least=6, at_most=10, spaces=False),
            roles=guests
        )

    def generate_post(func_author):
        return Post(
            title=lorem_ipsum.title(),
            body=lorem_ipsum.paragraphs(),
            created=date.date(),
            author=func_author(),
        )

    def generate_comment(func_author, func_post):
        return Comment(
            body=lorem_ipsum.paragraphs(),
            created=date.date(past=True),
            authors=func_author(),
            post=func_post()
        )


    users = [generate_user() for i in range(0, 5)]
    db.session.add_all(users)

    random_user = lambda: users[randint(0, 4)]
    posts = [generate_post(random_user) for i in range(0, randint(50, 200))]
    db.session.add_all(posts)

    random_post = lambda: posts[randint(0, len(posts) - 1)]

    comments = [generate_comment(random_user, random_post) for i in range(0, randint(2, 100))]
    db.session.add_all(comments)

    db.session.commit()






# @manager.command
# # 将dev命令加入到manager的命令中
# def dev():
#     from livereload import Server
#     live_server = Server(app.wsgi_app)
#     # 实例化监控对象
#     live_server.watch('**/*.*')
#     # 监控文件夹所有内容 **/*.*，也可以监控部分文件变动，例如static/*.*
#     live_server.serve(open_url_delay=1)
#     # 调试状态为真

if __name__ == '__main__':
    # virtualenv path E:\jinlinlin\virtualenv\flask_virtual_py27\scripts
    manager.run()
    # app.run(debug=True, extra_files=[os.path.join(app.root_path, app.template_folder)])