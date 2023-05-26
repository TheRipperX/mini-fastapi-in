from sqlalchemy.orm.session import Session
from model.base_models import *
from database.db_table import PostUser, User

from datetime import datetime


# create a new post
def create_post(token: Login_Model_Token, posts: Post_Model, db: Session):
    message = {"status": 0}

    try:
        token_login = db.query(User).filter(User.token_user == token.token).first()

        if token_login is None:
            message["data"] = "token not found..."
            return message
        
        if token_login.token_user == token.token:
            date_now = datetime.now()

            post = PostUser(
                title=posts.title, 
                description=posts.description,
                public = posts.public,
                date_make=date_now,
                user_id=token_login.id
            )

            db.add(post)
            db.commit()
            db.refresh(post)

            message["status"] = 1
            message["data"] = post
            return message


        else:
            message["data"] = "token is incorrect..."
            return message
    except:
        message["data"] = "server error invalid items..."
        return message


# show all posts
def show_posts(token: Show_Post_User, db: Session):
    message = {"status": 0}

    try:
        query_user = db.query(User).filter(User.token_user == token.token).first()

        if query_user is None:
            message["data"] = "token not found..."
            return message

        user_id = query_user.id

        query_post = db.query(PostUser).filter(PostUser.user_id == user_id).all()

        if query_post is None:  
            message["data"] = "no post user..."
            return message

        message["status"] = 1
        message["data"] = {
            "user":{"name": query_user.name, "username": query_user.username},
            "post": {"count_post": len(query_post), "posts": query_post}
            }
        
        return message


    except:
        message["data"] = "server error invalid items..."
        return message
