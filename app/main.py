from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published: bool = True

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

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def view_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    cursor.execute("""INSERT INTO posts(title,content,published) VALUES(%s,%s,%s) RETURNING * """,
                   (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data":new_post}

@app.get("/posts/{id}")
def view_post(id: int):
    post = get_correct_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Path not found")
    return {"data":post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    index = get_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")
    post_arr.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    index = get_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")
    post_dict = post.dict()
    post_dict["id"] = id
    post_arr[index] = post_dict
    return {"message":"updated successfully"}