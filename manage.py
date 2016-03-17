from gevent import monkey
monkey.patch_all()


from presentation import app, socketio, db
from flask.ext.script import Manager, Shell

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def runserver():
    socketio.run(app, "127.0.0.1", port=5001)

if __name__ == '__main__':
    manager.run()
