from decouple import config 


class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQL_ALCHEMY_TRACK_MODIFICATIONS = config('SQL_ALCHEMY_TRACK_MODIFICATIONS', cast = bool)

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://mark:2580_Mark@localhost/rev_eng"
    DEBUG = True
    SQLALCHEMY_ECHO = True 


class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass