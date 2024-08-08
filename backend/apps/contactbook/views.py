from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.contactbook.api_schemas import (
    contact_book_list_docs,
    contact_book_create_docs,
    contact_book_retrieve_docs,
)
from apps.contactbook.models import ContactBook
from apps.contactbook.serializers import (
    ContactBookRetrieveSerializer,
    ContactBookListSerializer,
    ContactBookLabelSerializer,
)
from apps.contactbook.service import contact_book_service


@extend_schema_view(
    list=contact_book_list_docs,
    create=contact_book_create_docs,
    retrieve=contact_book_retrieve_docs,
)
class ContactBookViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ContactBook.objects.all()
    filter_backends = [OrderingFilter]
    ordering = ["-created_datetime"]
    ordering_fields = [
        "created_datetime",
        "name",
        "email",
        "phone",
    ]

    def get_serializer_class(self):
        if self.action == "list":
            return ContactBookListSerializer
        return ContactBookRetrieveSerializer

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user).prefetch_related(
            "labels"
        )

    @extend_schema(
        summary="연락처 라벨 추가",
        description="연락처에 라벨을 추가하는 API",
        tags=["ContactBook Label"],
        request=ContactBookLabelSerializer,
    )
    @action(
        detail=True,
        methods=["POST"],
        url_path="label",
        serializer_class=ContactBookLabelSerializer,
    )
    def add_label(self, request, version=None, pk=None):
        contact = self.get_object()
        serializer = ContactBookLabelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = serializer.save(contact=contact, owner=request.user)
        return Response(
            ContactBookRetrieveSerializer(results).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="연락처 라벨 삭제",
        description="연락처에 등록된 라벨을 삭제하는 API",
        tags=["ContactBook Label"],
        request=ContactBookLabelSerializer,
    )
    @action(
        detail=True,
        methods=["POST"],
        url_path="label/deleted",
        serializer_class=ContactBookLabelSerializer,
    )
    def delete_label(self, request, version=None, pk=None):
        instance = self.get_object()
        serializer = ContactBookLabelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        labels = serializer.validated_data["labels"]
        labels = contact_book_service.get_labels(labels)
        instance.labels.filter(id__in=labels).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
