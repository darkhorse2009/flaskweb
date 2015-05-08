# import os
from app import create_app

from flask.ext.script import Manager, Server

app = create_app('testing')
manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0'))

if __name__ == '__main__':
    manager.run()