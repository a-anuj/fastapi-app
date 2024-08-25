from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    rating : Optional[int] = None

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def posts():
    return {"post":"Welcome to my page!"}

@app.post("/create/post")
def create_post(post:Post):
    post.dict()
    return {"data":post}
