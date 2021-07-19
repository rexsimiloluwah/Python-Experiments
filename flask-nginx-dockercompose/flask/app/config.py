import os 

class Config:
    DEBUG=False 
    BASE_DIR=os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_ECHO=False
    # SQLALCHEMY_TRACK_MODIFICATIONS=True
    SECRET_KEY='justsomethinghere'
    WTF_CSRF_SECRET_KEY='justsomethinghere'

class DevelopmentConfig(Config):
    DEBUG=True
    USERNAME = os.getenv('DB_USER','phpmyadmin')
    PASSWORD = os.getenv('DB_PASSWORD','adetoyosi')
    SERVER = os.getenv('DB_HOST','localhost')
    DATABASE = os.getenv('DB_NAME', 'flasko')
    SQLALCHEMY_DATABASE_URI = f"mysql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}"

