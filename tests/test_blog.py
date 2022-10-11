import pytest
# from model_bakery import baker
from rest_framework.test import APIClient
from account.models import Blog
# from tests.test_user_new import test_login_user

client = APIClient()


@pytest.mark.django_db
def test_get_all_blogs():
    response = client.get("/api/allblogs/")
    print(response.content)
    assert 1


@pytest.mark.django_db
def test_get_blog():
    # headers = {
    #     'Accept': 'application/json',
    #     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1MTQ2OTQ1LCJpYXQiOjE2NjUxMjg5NDUsImp0aSI6IjRjOGQ4OGZkMGJjOTQyNzBhN2Y4M2Q3ZDU0MDJjMDFlIiwidXNlcl9pZCI6ODB9.06KcHXOrjWr3og6DbzMyc-Kc1LzjNdnzgLPD9bwDAFA'
    # }
    client.credentials(HTTP_AUTHORIZATION='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1MzkzODAyLCJpYXQiOjE2NjUzNzU4MDIsImp0aSI6IjJlM2VhYWUxNjIyMzQwZDliNmY4ZDAyNTNkMTRmYmM3IiwidXNlcl9pZCI6ODB9.Lpevx2Mm6OMaN2B8rPjenoE3JU1p6kgX8OjWzamuudo')
   
    response = client.get("/api/blog/")
    print('jjjjj', response)
    assert 1


@pytest.mark.django_db
def test_create_blog():
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1MzkzODAyLCJpYXQiOjE2NjUzNzU4MDIsImp0aSI6IjJlM2VhYWUxNjIyMzQwZDliNmY4ZDAyNTNkMTRmYmM3IiwidXNlcl9pZCI6ODB9.Lpevx2Mm6OMaN2B8rPjenoE3JU1p6kgX8OjWzamuudo'  }

    client.credentials(HTTP_AUTHORIZATION='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1MzkzODAyLCJpYXQiOjE2NjUzNzU4MDIsImp0aSI6IjJlM2VhYWUxNjIyMzQwZDliNmY4ZDAyNTNkMTRmYmM3IiwidXNlcl9pZCI6ODB9.Lpevx2Mm6OMaN2B8rPjenoE3JU1p6kgX8OjWzamuudo')
    image = "E:\Harsh_Photos\Jui photos\IMG_9036.JPG"
    payload = dict(
        title='blog test',
        description='jdadadada  ad asd asdasddadasd',
        image=(open(image, 'rb'), image),
        user='80'

    )
    response = client.post("/api/blog/", payload, headers=headers)
    print(response.content)
    print(response.data)
    assert 1


@pytest.mark.django_db
def test_update_blog():
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1MzkzODAyLCJpYXQiOjE2NjUzNzU4MDIsImp0aSI6IjJlM2VhYWUxNjIyMzQwZDliNmY4ZDAyNTNkMTRmYmM3IiwidXNlcl9pZCI6ODB9.Lpevx2Mm6OMaN2B8rPjenoE3JU1p6kgX8OjWzamuudo'  
    }

    client.credentials(HTTP_AUTHORIZATION='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1MzkzODAyLCJpYXQiOjE2NjUzNzU4MDIsImp0aSI6IjJlM2VhYWUxNjIyMzQwZDliNmY4ZDAyNTNkMTRmYmM3IiwidXNlcl9pZCI6ODB9.Lpevx2Mm6OMaN2B8rPjenoE3JU1p6kgX8OjWzamuudo') 
    image = "E:\Harsh_Photos\Jui photos\IMG_9868.JPG"
    payload = dict(
        name='blog test update',
        description='jdadadada  ad asd asdasddadasd',
        image=(open(image, 'rb'), image),
        user='80'
    )
    response = client.put("/api/blog/42", payload, headers=headers)
    print(response.content)
    print(response.data)
    assert 1


@pytest.mark.django_db
def test_update_blog():
    client.credentials(HTTP_AUTHORIZATION='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY1MzkzODAyLCJpYXQiOjE2NjUzNzU4MDIsImp0aSI6IjJlM2VhYWUxNjIyMzQwZDliNmY4ZDAyNTNkMTRmYmM3IiwidXNlcl9pZCI6ODB9.Lpevx2Mm6OMaN2B8rPjenoE3JU1p6kgX8OjWzamuudo')
    response = client.delete("/api/blog/28")
    print(response.content)
    assert 1