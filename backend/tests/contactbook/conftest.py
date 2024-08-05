import pytest

from apps.contactbook.factories import ContactBookFactory, ContactLabelFactory
from apps.label.factories import LabelFactory


@pytest.fixture
def user_contact_book(user):
    return ContactBookFactory.create(owner=user)


@pytest.fixture
def labels(user):
    return LabelFactory.create_batch(10, owner=user)


@pytest.fixture
def label(user):
    return LabelFactory.create(owner=user)


@pytest.fixture
def contact_label(user_contact_book, label):
    return ContactLabelFactory.create(contact=user_contact_book, label=label)


@pytest.fixture
def contact_labels(user_contact_book):
    return ContactLabelFactory.create_batch(contact=user_contact_book)
