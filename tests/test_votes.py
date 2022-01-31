import pytest
from app import models

@pytest.fixture()
def test_sample_post_with_vote(sample_posts, session, test_user):
    new_vote=models.Votes(social_media_post_id=sample_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote(authorized_client, sample_posts):
    response = authorized_client.post("/vote/", json={"social_media_post_id": sample_posts[3].id, "voted":True})
    assert response.status_code == 201

def test_already_voted(authorized_client, sample_posts, test_sample_post_with_vote):
    response = authorized_client.post("/vote/", json={"social_media_post_id": sample_posts[3].id, "voted":True})
    assert response.status_code == 409

def test_remove_vote(authorized_client, sample_posts, test_sample_post_with_vote):
    response = authorized_client.post("/vote/", json={"social_media_post_id": sample_posts[3].id, "voted":False})
    assert response.status_code == 201

def test_try_to_remove_vote_not_previously_voted(authorized_client, sample_posts):
    response = authorized_client.post("/vote/", json={"social_media_post_id": sample_posts[3].id, "voted":False})
    assert response.status_code == 404

def test_vote_unavailable_post(authorized_client, sample_posts):
    response = authorized_client.post("/vote/", json={"social_media_post_id": 88888, "voted":True})
    assert response.status_code == 404

def test_vote_unauthorized_user(client,sample_posts):
    response = client.post("/vote/", json={"social_media_post_id": sample_posts[3].id, "voted":True})
    assert response.status_code == 401