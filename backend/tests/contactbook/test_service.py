import pytest
from unittest.mock import patch

from django.db.utils import IntegrityError

from apps.contactbook.service import ContactBookService


@pytest.mark.django_db
@patch("apps.contactbook.models.ContactLabel.objects.get_or_create")
def test_add_label_to_contact_book(
    mock_get_or_create, user_contact_book, labels
):
    label_id = labels[0].id
    ContactBookService.add_label(user_contact_book.id, [label_id])
    assert mock_get_or_create.call_count == 1


@pytest.mark.django_db
@patch("apps.contactbook.models.ContactLabel.objects.get_or_create")
def test_add_multiple_labels_to_contact_book(
    mock_get_or_create, user_contact_book, labels
):
    count = 2
    input_label = [label.id for label in labels[:count]]
    ContactBookService.add_label(user_contact_book.id, input_label)
    assert mock_get_or_create.call_count == count


@pytest.mark.django_db
def test_add_label_to_nonexistent_contact_book():
    labels = [100000]
    with pytest.raises(IntegrityError):
        ContactBookService.add_label(999, labels)
