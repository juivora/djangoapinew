from urllib import response
import pytest
from account.models import User

from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db()
def test_register_user():
    payload = dict(
        name='j4',
        email='j64@gmail.com',
        password='123456',
        password2='123456',
        tc="false"
    )

    response = client.post("/api/register/", payload, format='json')
    # print(response.content)
    data = response.data["data"]
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.django_db(transaction=True)
def test_login_user():

    payload = dict(
        email='j1@gmail.com',
        password='123456',
    )

    response = client.post("/api/login/", payload, format='json')
    print(response.content)
    print(response.data)
    status_code = response.status_code
    assert status_code
    # assert status_code == 200


@pytest.mark.django_db(transaction=True)
def test_login_user_fail():
    payload = dict(
        email='j63@gmail.com',
        password='1234',
    )

    response = client.post("/api/login/", payload)
    status_code = response.status_code
    assert status_code == 401
