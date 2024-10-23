import os

class Config:
    SECRET_KEY = os.urandom(24)
    DB_INFO = {
        'user': 'postgres',
        'password': 'sosuke812',
        'host': 'localhost',
        'name': 'postgres',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg://{user}:{password}@{host}/{name}'.format(**DB_INFO)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'sogari812@gmail.com'
    MAIL_PASSWORD = 'pjov vuzh ozqa usel'

