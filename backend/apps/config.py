import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///nestcare.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "JAI_SHRI_RAM_JAI_SHRI_KRISHNA"
    UPLOAD_EXTENSIONS = ['pdf']
    UPLOAD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', "pdf")
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 0
    CACHE_REDIS_URL = "redis://localhost:6379"  
    CACHE_DEFAULT_TIMEOUT = 500
    JWT_SECRET_KEY = 'JAI_SHRI_RAM'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mygmail.com'
    MAIL_PASSWORD = 'nopassword' 
    MAIL_DEFAULT_SENDER = 'noname'
