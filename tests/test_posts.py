from typing import List
from app import schemas
from tests.conftest import client
import pytest


def test_get_all_posts(authorized_client,test_posts):
    response = authorized_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate,response.json())
    post_list = list(post_map)
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client,test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_posts(client,test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
    response = authorized_client.get(f"/posts/90090")
    assert response.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title,content,published",[
    ("First title","First Content", True),
    ("Second title","Second Content", True),
    ("Third title","Third Content", False),
])
def test_create_post(authorized_client,test_user,test_posts,title,content,published):
    response = authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]

def test_create_post_published_true(authorized_client,test_user,test_posts):
    response = authorized_client.post("/posts/",json={"title":"fun","content":"funcontent"})
    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == "fun"
    assert created_post.content == "funcontent"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]

def test_unauthorized_user_create_post(client,test_user,test_posts):
    response = client.post("/posts/",json={"title":"fun","content":"funcontent"})
    assert response.status_code == 401

def test_unauthorized_user_delete_post(client,test_user,test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_success(authorized_client,test_posts,test_user):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_not_exist(authorized_client,test_posts,test_user):
    response = authorized_client.delete(f"/posts/9009")
    assert response.status_code == 404

def test_delete_other_user_post(authorized_client,test_posts,test_user):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403

