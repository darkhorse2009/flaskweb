from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mysqldb import MySQL
from config import config

bootstrap = Bootstrap()
mysql = MySQL()

#app initial
def create_app(configName):
    app = Flask(__name__)
    app.config.from_object(config[configName])

    bootstrap.init_app(app)
    mysql.init_app(app)

    from .lte import lteBlueprint
    app.register_blueprint(lteBlueprint)
    from .cdma import cdmaBlueprint
    app.register_blueprint(cdmaBlueprint)
    from .main import mainBlueprint
    app.register_blueprint(mainBlueprint)

    return app
