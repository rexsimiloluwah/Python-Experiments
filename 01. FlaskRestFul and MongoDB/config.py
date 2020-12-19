""" Configuration file for the entire aplication """
import os
from dotenv import load_dotenv
APP_ROOT = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(APP_ROOT, '.env')
load_dotenv(dotenv_path)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")


class Config:
    """Base Configuration"""
    DEBUG = False
    TESTING = False 
    DEVELOPMENT = True 
    SECRET_KEY = SECRET_KEY
    JWT_SECRET_KEY = JWT_SECRET_KEY
    # JWT_BLACKLIST_ENABLED = True
    # JWT_BLACKLIST_TOKEN_CHECKS = ['access','refresh']
    MONGODB_SETTINGS = {
        'host' : MONGO_URI
    }

class DevelopmentConfig(Config):
    """Development config"""
    DEBUG = True 
    MONGODB_SETTINGS = {
        'host' : MONGO_URI
    }

class ProductionConfig(Config):
    """Production Config"""
    DEBUG = False 
    MONGODB_SETTINGS = {
        'host' : MONGO_URI
    }