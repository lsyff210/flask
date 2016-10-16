from app import create_app, db
from flask_script import Manager, Server, Shell
from app.models import Role, User, State, Thing
from flask_migrate import Migrate, MigrateCommand, upgrade
import os

app = create_app()
manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, State=State, Thing=Thing)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver',
                    Server(
                        use_debugger=True,
                        use_reloader=True,
                        extra_files=[os.path.join(app.root_path, app.template_folder),
                                     os.path.join(app.root_path, app.template_folder, 'includes'),
                                     os.path.join(app.root_path, app.static_folder, 'css'),
                                     os.path.join(app.root_path, app.static_folder, 'js'),
                                     ],
                    ),

                )

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    from app.models import Role
    upgrade()
    Role.seed()


if __name__ == '__main__':
    # E:\jinlinlin\virtualenv\flask_work\Scripts
    manager.run()
