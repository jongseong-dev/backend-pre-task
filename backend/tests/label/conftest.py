from apps.label.factories import LabelFactory
import pytest


@pytest.fixture
def label(user):
    return LabelFactory.create(owner=user)
