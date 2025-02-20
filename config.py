from decouple import config 


class Config:
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', cast = bool)

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')
    DEBUG = False
    DB_USERNAME= config('DB_USERNAME')
    DB_PASSWORD= config('DB_PASSWORD')
    DB_HOST= config('DB_HOST')
    DB_PORT=3306
    DB_NAME= config('DB_NAME')
    SQLALCHEMY_ECHO = False 


class ProdConfig(Config):
    pass

class TestConfig(Config):
    pass
