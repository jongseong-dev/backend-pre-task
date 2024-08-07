from apps.label.models import Label


class ContactBookService:
    @staticmethod
    def add_label(
        instance,
        labels: list[int],
    ):
        for label in labels:
            if (
                label
                and Label.objects.owner(instance.owner)  # noqa: W503
                .filter(id=label)
                .exists()
            ):
                instance.labels.add(label)

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
