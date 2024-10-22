from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABASE_URI = "postgresql://guvi_yby8_user:MFyUGk2fbpvmiRZ8FaXIBt56uXD9eMWc@dpg-cmmvudocmk4c73e4qfh0-a.oregon-postgres.render.com:5432/guvi_yby8"
DATABASE_URI = "postgresql://postgres:ags009@localhost:5432/guvi"
engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def CreateTables():
     Base.metadata.create_all(bind=engine)

def get_db():
     db = SessionLocal()
     try:
          yield db
     finally:
          db.close()
          