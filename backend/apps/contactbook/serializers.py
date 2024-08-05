from django.db import transaction
from rest_framework import serializers

from apps.contactbook.models import ContactBook
from apps.contactbook.service import contact_book_service
from apps.label.models import Label
from apps.label.serializers import LabelSerializer


class ContactLabelSerializer(serializers.Serializer):
    """
    연락처에서 필요한 라벨에 대한 정보를 담고있는 Serializer
    1. write_only: label_ids - 라벨 ID를 입력으로 받는다.
    2. read_only: labels - 라벨 정보를 중첩된 구문으로 보여준다.
    """

    labels = serializers.SerializerMethodField(help_text="라벨 목록")
    label_ids = serializers.ListField(
        write_only=True,
        required=False,
        child=serializers.IntegerField(),
        help_text="라벨 ID",
    )

    def get_labels(self, obj) -> list[dict]:
        label_ids = [labeled.label_id for labeled in obj.labeled_contact.all()]
        labels = Label.objects.filter(id__in=label_ids)
        return LabelSerializer(labels, many=True).data

    class Meta:
        fields = ["labels", "label_ids"]


class ContactBookBaseSerializer(serializers.ModelSerializer):
    """
    주소록의 기본이 되는 Serializer 클래스
    해당 클래스를 상속받는 Serializer가 많으므로, 공통 요소가 아닌 이상은 편집하지 않는 것을 권장함
    """

    profile_image_url = serializers.URLField(help_text="프로필 이미지 URL")
    name = serializers.CharField(help_text="이름")
    email = serializers.EmailField(help_text="이메일")
    phone = serializers.CharField(help_text="전화번호")
    company = serializers.CharField(help_text="회사")
    position = serializers.CharField(help_text="직책")
    memo = serializers.CharField(help_text="메모")
    address = serializers.CharField(help_text="주소")
    birthday = serializers.DateField(
        help_text="생일",
        format="%Y-%m-%d",
        input_formats=["%Y-%m-%d"],
    )
    website_url = serializers.URLField(help_text="웹사이트 URL")

    class Meta:
        models = ContactBook


class ContactBookListSerializer(
    ContactLabelSerializer,
    ContactBookBaseSerializer,
    serializers.ModelSerializer,
):
    company_position = serializers.SerializerMethodField(
        help_text="회사(직책)"
    )

    def get_company_position(self, obj) -> str:
        return f"{obj.company}({obj.position})"

    class Meta:
        model = ContactBook
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "company_position",
            "profile_image_url",
            "labels",
        ]


class ContactBookUpdateDeleteSerializer(
    ContactBookBaseSerializer, serializers.ModelSerializer
):
    class Meta:
        model = ContactBook
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "company",
            "position",
            "memo",
            "profile_image_url",
            "address",
            "birthday",
            "website_url",
        ]


class ContactBookRetrieveSerializer(
    ContactLabelSerializer,
    ContactBookBaseSerializer,
    serializers.ModelSerializer,
):
    address = serializers.CharField(help_text="주소", required=False)
    birthday = serializers.DateField(help_text="생일", required=False)
    website_url = serializers.URLField(
        help_text="웹사이트 URL", required=False
    )

    def create(self, validated_data):
        with transaction.atomic():
            validated_data["owner"] = self.context["request"].user
            labels = validated_data.pop("label_ids", [])
            instance = super().create(validated_data)
            contact_book_service.add_label(instance.id, labels)
        return instance

    class Meta:
        model = ContactBook
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "company",
            "position",
            "memo",
            "profile_image_url",
            "address",
            "birthday",
            "website_url",
        ] + ContactLabelSerializer.Meta.fields


class ContactBookLabelSerializer(
    ContactLabelSerializer, serializers.Serializer
):
    class Meta:
        fields = ["label_ids"]

    def create(self, validated_data):
        with transaction.atomic():
            contact_id = validated_data["contact_id"]
            contact = ContactBook.objects.prefetch_related(
                "labeled_contact"
            ).get(id=contact_id)
            labels = validated_data.pop("label_ids", [])
            labels: list[int] = (
                Label.objects.owner(validated_data["owner"])
                .filter(id__in=labels)
                .values_list("id", flat=True)
            )
            contact_book_service.add_label(contact_id, labels)
            contact.refresh_from_db()
            return contact
