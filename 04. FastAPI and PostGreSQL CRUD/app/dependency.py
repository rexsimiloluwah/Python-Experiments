from config import engine, Session 

# Dependency for creating database session
def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()