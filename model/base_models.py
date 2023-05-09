from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime

# user model create account
class User_Model(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


# user model login account
class Login_Model(BaseModel):
    username: str
    password: str

#  login by token model
class Login_Model_Token(BaseModel):
    token: str


class Pay_Enum(str, Enum):
    day_30 = "30"
    day_60 = "60"
    day_90 = "90"


# create a new post
class Post_Model(BaseModel):
    title: str
    description: str
    public: Optional[bool] = None