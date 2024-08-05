from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from contactbook.models import ContactBook
from contactbook.serializers import (
    ContactBookRetrieveSerializer,
    ContactBookListSerializer,
    ContactBookUpdateDeleteSerializer,
    ContactBookLabelCreateSerializer,
)


@extend_schema(
    summary="주소록 API",
    description="주소록을 조회하는 API",
    tags=["ContactBook"],
)
class ContactBookViewSet(ModelViewSet):
    queryset = ContactBook.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
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
        if self.action in ["create", "retrieve"]:
            return ContactBookRetrieveSerializer
        return ContactBookUpdateDeleteSerializer

    def get_queryset(self):
        return self.queryset.filter(
            owner=self.request.user
        ).prefetch_related("labeled_contact")

    @extend_schema(
        summary="라벨 추가",
        description="주소록에 라벨을 추가하는 API",
        tags=["ContactBook"],
        request=ContactBookLabelCreateSerializer,
    )
    @action(
        detail=True,
        methods=["POST"],
        url_path="label",
        serializer_class=ContactBookLabelCreateSerializer,
    )
    def add_label(self, request, version=None, pk=None):
        serializer = ContactBookLabelCreateSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        results = serializer.save(
            contact_id=pk, owner=request.user
        )
        return Response(
            ContactBookRetrieveSerializer(results).data
        )
