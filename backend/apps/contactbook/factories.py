import factory
from faker import Faker

from apps.contactbook.models import ContactBook, ContactLabel
from apps.factories import UserFactory
from apps.label.factories import LabelFactory

fake = Faker("ko-KR")


class ContactBookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactBook

    owner = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"contact{n}")
    email = factory.LazyAttribute(lambda a: f"{a.name}@example.com")
    phone = factory.LazyAttribute(lambda x: fake.phone_number())
    company = factory.Sequence(lambda n: f"company{n}")
    position = factory.Sequence(lambda n: f"position{n}")
    memo = factory.Sequence(lambda n: f"memo{n}")
    profile_image_url = factory.Sequence(
        lambda n: f"http://example.com/profile{n}.jpg"
    )
    address = factory.Sequence(lambda n: f"address{n}")
    birthday = "2000-01-01"
    website_url = factory.Sequence(lambda n: f"http://example.com/{n}")


class ContactLabelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContactLabel

    contact = factory.SubFactory(ContactBookFactory)
    label = factory.SubFactory(LabelFactory)
