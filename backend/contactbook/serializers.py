from django.db import transaction
from phonenumber_field.serializerfields import (
    PhoneNumberField,
)
from rest_framework import serializers

from contactbook.models import ContactBook, ContactLabel
from label.models import Label
from label.serializers import LabelListSerializer


# TODO: 1. Serializer 정리
# TODO: 2. 중복되는 로직을 service layer로 이동시켜야 한다.
class ContactBookListSerializer(
    serializers.ModelSerializer
):
    profile_image_url = serializers.URLField(
        required=False, help_text="프로필 이미지 URL"
    )
    name = serializers.CharField(help_text="이름")
    email = serializers.EmailField(help_text="이메일")
    phone = serializers.CharField(help_text="전화번호")
    company = serializers.CharField(help_text="회사")
    position = serializers.CharField(help_text="직책")
    labels = LabelListSerializer(
        source="labeled_contact",
        many=True,
        read_only=True,
        help_text="라벨 목록",
    )

    class Meta:
        model = ContactBook
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "company",
            "position",
            "profile_image_url",
            "labels",
        ]


class ContactLabelListInputSerializer(
    serializers.Serializer
):
    label_ids = serializers.ListField(
        write_only=True,
        required=False,
        child=serializers.IntegerField(),
        help_text="라벨 ID",
    )

    class Meta:
        fields = ["label_ids"]


class ContactBookUpdateDeleteSerializer(
    serializers.ModelSerializer
):
    name = serializers.CharField(
        max_length=50, required=True, help_text="이름"
    )
    phone = PhoneNumberField(
        required=True, help_text="전화번호", region="KR"
    )
    email = serializers.EmailField(
        required=False, help_text="이메일"
    )
    company = serializers.CharField(
        max_length=50, required=False, help_text="회사"
    )
    position = serializers.CharField(
        max_length=50, required=False, help_text="직책"
    )
    memo = serializers.CharField(
        required=False, help_text="메모"
    )
    profile_image_url = serializers.URLField(
        required=False, help_text="프로필 이미지 URL"
    )
    address = serializers.CharField(
        max_length=100, required=False, help_text="주소"
    )
    birthday = serializers.DateField(
        required=False,
        help_text="생일",
        format="%Y-%m-%d",
        input_formats=["%Y-%m-%d"],
    )
    website_url = serializers.URLField(
        required=False, help_text="웹사이트 URL"
    )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

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
    ContactLabelListInputSerializer,
    ContactBookUpdateDeleteSerializer,
):
    labels = LabelListSerializer(
        source="labeled_contact",
        many=True,
        read_only=True,
        help_text="라벨 목록",
    )

    def create(self, validated_data):
        with transaction.atomic():
            validated_data["owner"] = self.context[
                "request"
            ].user
            instance = super().create(validated_data)
            labels = validated_data.pop("label_ids", [])
            if labels:
                for label in labels:
                    ContactLabel.objects.create(
                        contact=instance.id, label_id=label
                    )
        return instance

    class Meta(
        ContactLabelListInputSerializer.Meta,
        ContactBookUpdateDeleteSerializer.Meta,
    ):
        list_serializer_class = LabelListSerializer

        contact_book_meta = (
            ContactBookUpdateDeleteSerializer.Meta.fields
        )
        label_list_meta = (
            ContactLabelListInputSerializer.Meta.fields
        )
        fields = (
            contact_book_meta + label_list_meta + ["labels"]
        )


class ContactBookLabelCreateSerializer(
    ContactLabelListInputSerializer
):
    class Meta(ContactLabelListInputSerializer.Meta):
        fields = ContactLabelListInputSerializer.Meta.fields

    def create(self, validated_data):
        with transaction.atomic():
            contact_id = validated_data["contact_id"]
            contact = ContactBook.objects.prefetch_related(
                "labeled_contact"
            ).get(id=contact_id)
            labels = validated_data.pop("label_ids", [])
            labels: list[Label] = (
                Label.objects.owner(validated_data["owner"])
                .filter(id__in=labels)
                .only("id")
            )
            for label in labels:
                ContactLabel.objects.get_or_create(
                    contact_id=contact_id, label_id=label.id
                )
            contact.refresh_from_db()
            return contact
