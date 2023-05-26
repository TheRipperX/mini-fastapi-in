from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from database.db import get_session
from model.base_models import Post_Model, Login_Model_Token, Show_Post_User
from data import post_or_api


router = APIRouter(prefix="/post", tags=["Api Posts"])


@router.post("/create_post")
async def create_post(token: Login_Model_Token, posts: Post_Model, db = Depends(get_session)):

    if token.token is None or token.token == "" or posts is None or posts.title == "" or posts.description == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or empty data for new post")
    
    query_post = post_or_api.create_post(token, posts, db)

    return query_post


@router.post("/show_posts")
async def show_post_user(token: Show_Post_User, db = Depends(get_session)):

    if token.token is None or token.token == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or empty data for show post")
    
    query_show_post = post_or_api.show_posts(token, db)

    return query_show_post