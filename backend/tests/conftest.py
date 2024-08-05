import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.factories import UserFactory


@pytest.fixture
def plain_password():
    return "userpassword"


@pytest.fixture
def user(plain_password):
    return UserFactory(password=plain_password)


@pytest.fixture
def other_user(plain_password):
    return UserFactory(password=plain_password)


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def authenticated_user_client(client, user):
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def authenticated_other_user_client(client, other_user):
    refresh = RefreshToken.for_user(other_user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client
