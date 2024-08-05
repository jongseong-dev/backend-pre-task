import factory

from apps.factories import UserFactory
from apps.label.models import Label


class LabelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Label

    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"label{n}")
