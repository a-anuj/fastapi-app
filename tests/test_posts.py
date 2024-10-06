from typing import List
from app import schemas

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