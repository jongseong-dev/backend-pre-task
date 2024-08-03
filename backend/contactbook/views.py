from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from contactbook.models import ContactBook
from contactbook.serializers import (
    ContactBookRetrieveSerializer,
    ContactBookListSerializer,
)


@extend_schema(
    summary="주소록 API",
    description="주소록을 조회하는 API",
    tags=["ContactBook"],
)
class ContactBookViewSet(ModelViewSet):
    queryset = ContactBook.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ContactBookListSerializer
        return ContactBookRetrieveSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    @action(
        detail=True,
        methods=["get", "post", "update"],
        url_path="label",
        url_name="label",
    )
    def labeled_contactbook(self, request, pk=None):
        pass
