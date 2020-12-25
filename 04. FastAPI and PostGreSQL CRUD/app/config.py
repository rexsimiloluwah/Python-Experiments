import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.exc import SQLAlchemyError

# Loading database configuration for PostGreSQL connection
APP_ROOT = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(APP_ROOT, '.env'))

DBUSERNAME = os.getenv("DBUSERNAME")
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")
HOST = os.getenv("HOST")
DATABASE = os.getenv("DATABASE")

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


SQLALCHEMY_DATABASE_URI = f"postgresql://{DBUSERNAME}:{PASSWORD}@{SERVER}:{HOST}/{DATABASE}"

engine = create_engine(SQLALCHEMY_DATABASE_URI)

# Session maker - should always be in the same scope as the engine
Session = sessionmaker(bind = engine)
Base = declarative_base()
