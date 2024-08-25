from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    rating : Optional[int] = None

post_arr = [{"id":"1","title":"CSK","content":"5 trophies"},{"id":"2","title":"KKR","content":"3 trophies"}]

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def posts():
    return {"data":post_arr}

@app.post("/posts")
def create_post(post:Post):
    post.dict()
    return {"data":post}
