import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    DB_USER = os.environ.get('POSTGRES_USER', 'user')
    DB_PASS = os.environ.get('POSTGRES_PASSWORD', 'ultrasecret1')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5434')
    DB_NAME = os.environ.get('POSTGRES_DB', 'library_dev')
    
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:ultrasecret2@localhost:5435/library_prod'
