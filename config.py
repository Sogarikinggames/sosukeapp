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

