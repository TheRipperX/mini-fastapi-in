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
def show_posts():
    pass
