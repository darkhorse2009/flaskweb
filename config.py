import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_DB = 'testdb'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'fangww'
    MYSQL_PORT = 3365

class TestingConfig(Config):
    TESTING = True
    MYSQL_DB = 'data_test'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'fangww'
    MYSQL_PORT = 3365

class ProductionConfig(Config):
    MYSQL_DB = 'data_production'
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'fangww'
    MYSQL_PORT = 3365

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}