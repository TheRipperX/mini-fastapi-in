from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from model.base_models import *

from database.db import get_session
from database.db import Base

from data import user_or_api


router = APIRouter(prefix="/user", tags=["Api User"])


@router.post("/new_user")
async def new_user(user: User_Model, db = Depends(get_session)):

    if user.name == "" or user.email == "" or user.username == "" or user.password == "":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid or empty data for new user")
    
    # add user to database
    query = user_or_api.create_user(user, db)

    if query["status"] == "success":
        message = {}
        message["status"] = query["status"]

        message["data"] = {"name": user.name, "username": user.username, "email": user.email}

        return message

    else:
        return query
    


@router.post("/login")
async def login_user(user: Login_Model, db = Depends(get_session)):

    if user.username is None or user.password is None or user.password == "" or user.username == "":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid or empty data for login user ...")
    
    query = user_or_api.login_user(user, db)

    return query


@router.post("/token")
async def login_user_token(user: Login_Model_Token, db = Depends(get_session)):

    if user.token is None or user.token == "":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid or empty data for login user by token ...")
    
    query = user_or_api.login_user_by_token(user, db)

    return query


@router.post("/pay/{days}")
async def pay_user_app(user: Login_Model_Token, days: Pay_Enum , db = Depends(get_session)):

    if user.token is None or user.token == "" or days is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid or empty data for login user by token ...")
    
    query = user_or_api.pay_app(user, days , db)

    return query


@router.post("/info/user/")
async def info_user(user: Login_Model_Token, db = Depends(get_session)):

    if user.token is None or user.token == "":
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid or empty data for login user by token ...")
    
    query = user_or_api.info_user_account(user , db)

    return query