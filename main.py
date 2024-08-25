from typing import Optional

from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    rating : Optional[int] = None

post_arr = [{"id":1,"title":"CSK","content":"5 trophies"},{"id":2,"title":"KKR","content":"3 trophies"}]

def get_correct_post(id):
    for post in post_arr:
        if post['id'] == id:
            return post

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def view_posts():
    return {"data":post_arr}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1,1000000)
    post_arr.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/{id}")
def view_post(id: int):
    post = get_correct_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Path not found")
    return {"data":post}
