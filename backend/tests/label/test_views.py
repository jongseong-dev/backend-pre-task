import pytest
from rest_framework import status


@pytest.fixture
def label_url():
    return "/api/v1/label/"


@pytest.mark.django_db
def test_label_list_valid_access(authenticated_user_client, label_url, label):
    response = authenticated_user_client.get(
        label_url,
    )
    result = response.data
    assert response.status_code == status.HTTP_200_OK
    assert result["results"][0]["name"] == label.name


@pytest.mark.django_db
def test_label_list_invalid_access(client, label_url, label):
    response = client.get(
        label_url,
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_label_list_invalid_access_other_user(
    authenticated_other_user_client, label_url, label
):
    response = authenticated_other_user_client.get(label_url)
    result = response.data
    assert response.status_code == status.HTTP_200_OK
    assert len(result["results"]) == 0


@pytest.mark.django_db
def test_label_create_valid(authenticated_user_client, label_url):
    input_data = {"name": "test label"}
    response = authenticated_user_client.post(
        label_url,
        data=input_data,
    )
    result = response.data
    assert response.status_code == status.HTTP_201_CREATED
    assert result["name"] == input_data["name"]


@pytest.mark.django_db
def test_label_detail_valid(authenticated_user_client, label_url, label):
    url = f"{label_url}{label.id}/"
    response = authenticated_user_client.get(
        url,
    )
    result = response.data
    assert response.status_code == status.HTTP_200_OK
    assert result["name"] == label.name
