from fastapi import FastAPI

from database import db_table
from database.db import engin

from router import users_api


db_table.Base.metadata.create_all(engin)

app = FastAPI()

app.include_router(users_api.router)


@app.get("/")
def index():
    message = {"message":"Hello, world!"}

    return message
