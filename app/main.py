from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from . import models,schemas, utils
from .database import engine, get_db
from typing import List
from .routers import user, post

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi",user="postgres",
                                password="anuj2006",cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        break
    except Exception as error:
        print("Connection to database failed!")
        print("Error : ",error)
        time.sleep(2)


post_arr = [{"id":1,"title":"CSK","content":"5 trophies"},{"id":2,"title":"KKR","content":"3 trophies"}]

def get_correct_post(id):
    for post in post_arr:
        if post['id'] == id:
            return post

def get_post_index(id):
    for index,post in enumerate(post_arr):
        if post['id'] == id:
            return index

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message":"Hello World"}





