from django_filters.rest_framework import (
    DjangoFilterBackend,
)
from drf_spectacular.utils import extend_schema
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.contactbook.api_schemas import contact_book_parameters
from apps.contactbook.models import ContactBook
from apps.contactbook.serializers import (
    ContactBookRetrieveSerializer,
    ContactBookListSerializer,
    ContactBookUpdateDeleteSerializer,
    ContactBookLabelSerializer,
)


@extend_schema(
    summary="주소록 API",
    description="주소록을 조회하는 API",
    tags=["ContactBook"],
)
class ContactBookViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
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
        return self.queryset.filter(owner=self.request.user).prefetch_related(
            "labeled_contact"
        )

    @extend_schema(
        summary="연락처 생성 API",
        description="주소록의 연락처를 생성하는 API",
        request=ContactBookRetrieveSerializer,
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="연락처 목록을 조회하는 API",
        description="본인의 연락처 목록을 조회하는 API",
        parameters=contact_book_parameters,
        request=ContactBookListSerializer,
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="연락처 상세를 조회하는 API",
        description="본인의 연락처를 상세 조회한다.",
        request=ContactBookRetrieveSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

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
        results = serializer.save(contact_id=contact.id, owner=request.user)
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
        label_ids = serializer.validated_data["label_ids"]
        instance.labeled_contact.filter(label_id__in=label_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
