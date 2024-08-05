import pytest
from rest_framework import status

from apps.contactbook.factories import ContactBookFactory, ContactLabelFactory
from apps.label.models import Label


@pytest.fixture
def contact_book_url():
    return "/api/v1/contactbook/"


@pytest.mark.django_db
def test_contact_book_list_invalid_auth(client, contact_book_url):
    response = client.get(contact_book_url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_contact_book_list_valid(
    authenticated_user_client, contact_book_url, user
):
    count = 5
    ContactBookFactory.create_batch(count, owner=user)
    response = authenticated_user_client.get(contact_book_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == count


@pytest.mark.django_db
def test_contact_book_list_invalid_access_another_user(
    authenticated_other_user_client, contact_book_url, user
):
    ContactBookFactory.create_batch(5, owner=user)
    response = authenticated_other_user_client.get(contact_book_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 0


@pytest.mark.django_db
def test_contact_book_list_ordering(
    authenticated_user_client, contact_book_url, user
):
    items = ContactBookFactory.create_batch(5, owner=user)
    response = authenticated_user_client.get(contact_book_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == items[-1].id

    # 이름을 내림차순으로 정렬
    name_reverse_sorted_response = authenticated_user_client.get(
        f"{contact_book_url}?ordering=-name"
    )
    assert name_reverse_sorted_response.status_code == status.HTTP_200_OK
    items = sorted(items, key=lambda x: x.name)
    results = name_reverse_sorted_response.data["results"][0]["name"]
    assert results == items[-1].name

    # 전화번호를 내림차순으로 정렬
    phone_reverse_sorted_response = authenticated_user_client.get(
        f"{contact_book_url}?ordering=-phone"
    )
    assert phone_reverse_sorted_response.status_code == status.HTTP_200_OK
    items = sorted(items, key=lambda x: str(x.phone))
    results = phone_reverse_sorted_response.data["results"][0]["phone"]
    assert results == str(items[-1].phone)

    # 이메일을 내림차순으로 정렬
    email_reverse_sorted_response = authenticated_user_client.get(
        f"{contact_book_url}?ordering=-email"
    )
    assert email_reverse_sorted_response.status_code == status.HTTP_200_OK
    items = sorted(items, key=lambda x: x.email)
    results = email_reverse_sorted_response.data["results"][0]["email"]
    assert results == items[-1].email


@pytest.mark.django_db
def test_contact_retrieve_invalid_auth(
    client, contact_book_url, user_contact_book
):
    response = client.get(f"{contact_book_url}{user_contact_book.id}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_contact_book_retrieve_valid_auth(
    authenticated_user_client, contact_book_url, user_contact_book
):
    response = authenticated_user_client.get(
        f"{contact_book_url}{user_contact_book.id}/"
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_contact_book_retrieve_invalid_access_another_user(
    authenticated_other_user_client, contact_book_url, user_contact_book
):
    response = authenticated_other_user_client.get(
        f"{contact_book_url}{user_contact_book.id}/"
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_contact_book_retrieve_response_data(
    authenticated_user_client, contact_book_url, user_contact_book
):
    response = authenticated_user_client.get(
        f"{contact_book_url}{user_contact_book.id}/"
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == user_contact_book.id
    assert response.data["name"] == user_contact_book.name
    assert response.data["labels"] == []


@pytest.fixture
def contact_book_insert_data():
    return ContactBookFactory.build()


@pytest.fixture
def contact_book_post_insert_data(contact_book_insert_data):
    return {
        "name": contact_book_insert_data.name,
        "email": contact_book_insert_data.email,
        "phone": contact_book_insert_data.phone,
        "company": contact_book_insert_data.company,
        "position": contact_book_insert_data.position,
        "memo": contact_book_insert_data.memo,
        "profile_image_url": contact_book_insert_data.profile_image_url,
        "address": contact_book_insert_data.address,
        "birthday": contact_book_insert_data.birthday,
        "website_url": contact_book_insert_data.website_url,
    }


@pytest.mark.django_db
def test_contact_book_create(
    authenticated_user_client, contact_book_url, contact_book_post_insert_data
):
    response = authenticated_user_client.post(
        contact_book_url, data=contact_book_post_insert_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == contact_book_post_insert_data["name"]


@pytest.mark.django_db
def test_contact_book_create_invalid_required_empty(
    authenticated_user_client, contact_book_url, contact_book_post_insert_data
):
    # 핸드폰 번호 빠짐
    insert_data_phone_pop = contact_book_post_insert_data.copy()
    insert_data_phone_pop.pop("phone")
    response = authenticated_user_client.post(
        contact_book_url, data=insert_data_phone_pop
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["phone"][0] == "This field is required."

    # 이름 빠짐
    insert_data_name_pop = contact_book_post_insert_data.copy()
    insert_data_name_pop.pop("name")
    response = authenticated_user_client.post(
        contact_book_url, data=insert_data_name_pop
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["name"][0] == "This field is required."


@pytest.mark.django_db
def test_contact_book_create_with_label(
    authenticated_user_client,
    contact_book_url,
    contact_book_post_insert_data,
    labels,
):
    insert_data = contact_book_post_insert_data
    insert_data["label_ids"] = [label.id for label in labels]
    response = authenticated_user_client.post(
        contact_book_url,
        data=insert_data,
    )
    result = response.data
    assert response.status_code == status.HTTP_201_CREATED
    assert result["name"] == insert_data["name"]
    labels_results = [
        Label(id=label["id"], name=label["name"]) for label in result["labels"]
    ]
    assert labels_results == labels


@pytest.mark.django_db
def test_contact_book_add_label(
    authenticated_user_client,
    contact_book_url,
    user_contact_book,
    labels,
):
    contact_book_add_label_url = (
        f"{contact_book_url}{user_contact_book.id}/label/"
    )
    response = authenticated_user_client.post(
        contact_book_add_label_url,
        data={
            "label_ids": [label.id for label in labels[:5]],
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == user_contact_book.name
    assert response.data["labels"][0]["name"] == labels[0].name


@pytest.mark.django_db
def test_contact_book_add_label_access_other_user(
    authenticated_other_user_client,
    contact_book_url,
    user_contact_book,
    labels,
):
    contact_book_add_label_url = (
        f"{contact_book_url}{user_contact_book.id}/label/"
    )
    response = authenticated_other_user_client.post(
        contact_book_add_label_url,
        data={
            "label_ids": [label.id for label in labels[:5]],
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_contact_book_delete_label(
    authenticated_user_client,
    contact_book_url,
    user_contact_book,
    labels,
):
    for label in labels[:3]:
        ContactLabelFactory.create(contact=user_contact_book, label=label)

    contact_book_add_label_url = (
        f"{contact_book_url}{user_contact_book.id}/label/deleted/"
    )
    print("url:", contact_book_add_label_url)
    response = authenticated_user_client.post(
        contact_book_add_label_url,
        data={
            "label_ids": [label.id for label in labels],
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_contact_book_delete_label_access_other_user(
    authenticated_other_user_client,
    contact_book_url,
    contact_label,
    labels,
):
    contact_book_delete_label_url = (
        f"{contact_book_url}{contact_label.contact.id}/label/deleted/"
    )
    response = authenticated_other_user_client.post(
        contact_book_delete_label_url,
        data={
            "label_ids": [contact_label.label.id],
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
