from sqlalchemy.orm.session import Session
from database.db_table import PostUser


# show all posts index items
def get_posts(db: Session):
    message = {"status": 0}
    try:
        query_all_post = db.query(PostUser).all()
        if query_all_post is None:
            message["data"] = "no posts found for database"
            return message
        
        message["status"] = 1
        message["data"] = query_all_post
        return message

    except:
        message["data"] = "error getting posts"
        return message