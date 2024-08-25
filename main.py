from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return {"message":"Hello World"}

@app.get("/posts")
def posts():
    return {"post":"Welcome to my page!"}

@app.post("/create/post")
def create_post(payload: dict=Body(...)):
    return {"title":payload['title'],
            "content":payload['content']
            }