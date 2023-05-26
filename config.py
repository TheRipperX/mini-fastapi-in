from fastapi import FastAPI

from fastapi import Depends

from database import db_table
from database.db import engin, get_session

# show all posts class
from data.index_or_api import get_posts

from router import users_api, post_api


db_table.Base.metadata.create_all(engin)

app = FastAPI()

app.include_router(users_api.router)
app.include_router(post_api.router)


@app.get("/")
def index(db = Depends(get_session)):
    data = get_posts(db)

    return data
