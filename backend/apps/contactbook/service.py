from apps.contactbook.models import ContactLabel


class ContactBookService:
    @staticmethod
    def add_label(contact_id: int, labels: list[int]):
        for label in labels:
            ContactLabel.objects.get_or_create(
                contact_id=contact_id, label_id=label
            )


contact_book_service = ContactBookService()
