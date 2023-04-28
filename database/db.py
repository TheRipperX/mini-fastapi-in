from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engin = create_engine("sqlite:///Instageeam.db", connect_args={"check_same_thread":False})
Base = declarative_base()
sessionMaker = sessionmaker(bind=engin)

def get_session():
    session = sessionMaker()

    try:
        yield session
    finally:
        session.close()    