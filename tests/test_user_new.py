import pytest
from rest_framework.test import APIClient
from account.models import User

client = APIClient()


# class TestUserClass:

@pytest.fixture(scope="session")
def httpserver():
    return ("localhost", 8000)


@pytest.fixture()
@pytest.mark.django_db()
def test_create_user():
    user = User.objects.create(
        name='j4',
        email='j4@gmail.com',
        password='123456',
        tc=False)

    return user


@pytest.mark.django_db()
def test_login_user(test_create_user):
    print(test_create_user.email)
    print(test_create_user.password)
    # print(self.user)

    payload = {
        'email': 'j1@gmail.com',
        'password': test_create_user.password,
    }

    response = client.post("/api/login/", payload, format='json')
    print(response.content)
    print(response.data)
    status_code = response.status_code

    return response.data
    # assert status_code
    # # assert status_code == 200
    # # assert True
