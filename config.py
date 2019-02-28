class Config(object):
    pass
class ProdConfig(Config):
    pass
class DevConfig(Config):
    DEBUG = True
    SQLALCHMEY_ECHO = True
    SQLALCHEMY_DATABASE_URI ="sqlite:///database.db"
