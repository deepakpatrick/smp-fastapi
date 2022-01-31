from importlib.resources import contents
from venv import create
from app import schemas
import pytest


def test_get_all_posts(authorized_client, sample_posts):
    response = authorized_client.get("/posts/")
    print(response.json())
    def validate(post):
        print(post)
        return schemas.BaseSocialMediaPostResponses(**post)
    posts_map = map(validate, response.json())
    #print(list(posts_map))
    assert len(response.json()) == len(sample_posts)
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client, sample_posts):
    response = client.get("/posts/")
    assert response.status_code == 200 # we actually allow unauthorized users to get all posts

def test_unauthorized_user_get_one_post(client, sample_posts):
    response = client.get(f"/posts/{sample_posts[0].id}")
    assert response.status_code == 401  

def test_user_get_one_unavailable_post(authorized_client, sample_posts):
    response = authorized_client.get("/posts/56778")
    assert response.status_code == 404

def test_user_get_one_post(authorized_client, sample_posts):
    response = authorized_client.get(f"/posts/{sample_posts[0].id}")
    post = schemas.PostsWithOwnerVotesInfo(**response.json())
    assert post.SocialMediaPosts.id == sample_posts[0].id
    assert post.SocialMediaPosts.contents == sample_posts[0].contents
    assert response.status_code == 200

@pytest.mark.parametrize("title,contents,published",[
    ('title-a','title-a-contents',True),
    ('title-b','title-b-contents',False),
    ('title-c','title-c-contents',True),
    ('title-d','title-d-contents',False)
])
def test_create_post(authorized_client, sample_posts, test_user, title, contents, published):
    response = authorized_client.post(f"/posts/",json={"title":title, "contents":contents, "published":published})
    created_post = schemas.BaseSocialMediaPostResponses(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.contents == contents
    assert created_post.published == published
    assert created_post.owner.id == test_user['id']

def test_check_default_published_true(authorized_client, sample_posts, test_user):
    response = authorized_client.post(f"/posts/",json={"title":'something', "contents":'somecontents'})
    created_post = schemas.BaseSocialMediaPostResponses(**response.json())
    assert response.status_code == 201    
    assert created_post.published == True

def test_unauthorized_user_create_posts(client, test_user, sample_posts):
    response = client.post(f"/posts/",json={"title":'something', "contents":'somecontents'})
    assert response.status_code == 401

def test_unauthorized_delete_post(client, test_user, sample_posts):
    response = client.delete(f"/posts/{sample_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_success(authorized_client, test_user, sample_posts):
    response = authorized_client.delete(f"/posts/{sample_posts[0].id}")
    assert response.status_code == 204

def test_delete_unavailable_post(authorized_client, test_user, sample_posts):
    response = authorized_client.delete("/posts/342342")
    assert response.status_code == 404

def test_delete_post_created_by_another_user(authorized_client, test_user, sample_posts):
    response = authorized_client.delete(f"/posts/{sample_posts[3].id}") # 4th post is from test_user2
    assert response.status_code == 403

def test_update_post(authorized_client, test_user, sample_posts):
    data = {
        "title":"updated post",
        "contents": "modified post",
        "id":sample_posts[0].id
    }
    response = authorized_client.put(f"/posts/{sample_posts[0].id}", json=data)
    updated_post = schemas.BaseSocialMediaPostRequests(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.contents == data['contents']
    
def test_update_another_user_post(authorized_client, test_user, sample_posts):
    data = {
        "title":"updated post",
        "contents": "modified post",
        "id":sample_posts[3].id
    }
    response = authorized_client.put(f"/posts/{sample_posts[3].id}", json=data)
    assert response.status_code == 403

def test_unauthorized_update_post(client, test_user, sample_posts):
    data = {
    "title":"updated post",
    "contents": "modified post",
    "id":sample_posts[3].id
    }
    response = client.put(f"/posts/{sample_posts[3].id}", json=data)
    assert response.status_code == 401

def test_update_unavailable_post(authorized_client, test_user, sample_posts):
    data = {
    "title":"updated post",
    "contents": "modified post",
    "id":sample_posts[0].id
    }
    response = authorized_client.put("/posts/342342",json=data)
    assert response.status_code == 404