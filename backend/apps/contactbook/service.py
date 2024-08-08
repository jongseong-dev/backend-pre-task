from apps.label.models import Label


class ContactBookService:
    @staticmethod
    def add_label(
        instance,
        labels: list[int],
    ):
        exist_labels = (
            Label.objects.owner(instance.owner)
            .filter(id__in=labels)
            .only("id")
        )
        instance.labels.set(exist_labels)

    @staticmethod
    def get_labels(
        request_labels: list[dict],
    ) -> list[int]:
        results = []
        for request_label in request_labels:
            if not request_label:
                continue
            results.append(request_label["id"])
        return results


contact_book_service = ContactBookService()
