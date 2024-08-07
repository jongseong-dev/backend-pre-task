from django.db import transaction
from rest_framework import serializers

from apps.contactbook.models import ContactBook
from apps.contactbook.service import contact_book_service


class ContactLabelSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="라벨 ID")
    name = serializers.CharField(help_text="라벨 이름", read_only=True)

    class Meta:
        fields = ["id", "name"]


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
    ContactBookBaseSerializer,
    serializers.ModelSerializer,
):
    company_position = serializers.SerializerMethodField(
        help_text="회사(직책)"
    )
    labels = ContactLabelSerializer(
        many=True,
        required=False,
        help_text="라벨",
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


class ContactBookRetrieveSerializer(
    ContactBookBaseSerializer,
    serializers.ModelSerializer,
):
    address = serializers.CharField(help_text="주소", required=False)
    birthday = serializers.DateField(help_text="생일", required=False)
    website_url = serializers.URLField(
        help_text="웹사이트 URL", required=False
    )
    labels = ContactLabelSerializer(many=True, required=False)

    @transaction.atomic
    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        labels = validated_data.pop("labels", [{}])
        instance: ContactBook = super().create(validated_data)
        labels = contact_book_service.get_labels(labels)
        contact_book_service.add_label(instance, labels)
        return instance

    class Meta:
        model = ContactBook
        list_serializer_class = ContactLabelSerializer
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
            "labels",
        ]


class ContactBookLabelSerializer(serializers.Serializer):
    labels = ContactLabelSerializer(many=True)

    class Meta:
        fields = ["labels"]

    @transaction.atomic
    def create(self, validated_data):
        instance: ContactBook = validated_data["contact"]
        labels = validated_data.pop("labels", [{}])
        labels = contact_book_service.get_labels(labels)
        contact_book_service.add_label(instance, labels)
        return instance
