import pytest


from apps.contactbook.service import ContactBookService


@pytest.mark.django_db
def test_add_label_to_contact_book(user_contact_book, label):
    labels = [label.id]
    ContactBookService.add_label(user_contact_book, labels)
    assert user_contact_book.labels.first().id == label.id


@pytest.mark.django_db
def test_add_label_to_contact_book_no_label(user_contact_book):
    labels = [9999]
    ContactBookService.add_label(user_contact_book, labels)
    assert not user_contact_book.labels.first()


@pytest.mark.django_db
def test_get_labels():
    request_labels = [{"id": 1}, {"id": 2}]
    result = ContactBookService.get_labels(request_labels)
    assert result == [1, 2]


@pytest.mark.django_db
def test_get_labels_empty():
    request_labels = []
    result = ContactBookService.get_labels(request_labels)
    assert result == []
