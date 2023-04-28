from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    date_buy = Column(DateTime, nullable=True)
    date_end = Column(DateTime, nullable=True)
    is_pro = Column(Boolean, default=False)
    token_user = Column(String, nullable=True)


