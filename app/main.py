from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)
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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.get("/posts")
def view_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
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
    cursor.execute("""SELECT * FROM posts where id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Path not found")
    return {"data":post}

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts where id=%s returning *""",(id,))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute("""UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s returning *""",(post.title,post.content,post.published,id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="id not found")
    return {"data":updated_post}