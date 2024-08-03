from phonenumber_field.serializerfields import (
    PhoneNumberField,
)
from rest_framework import serializers

from contactbook.models import ContactBook, ContactLabel


class ContactBookListSerializer(serializers.ListSerializer):
    profile_image_url = serializers.URLField(
        required=False, help_text="프로필 이미지 URL"
    )
    name = serializers.CharField(help_text="이름")
    email = serializers.EmailField(help_text="이메일")
    phone = serializers.CharField(help_text="전화번호")
    company = serializers.CharField(help_text="회사")
    position = serializers.CharField(help_text="직책")


class ContactBookRetrieveSerializer(
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

    def create(self, validated_data):
        validated_data["owner"] = self.context[
            "request"
        ].user
        return super().create(validated_data)

    class Meta:
        model = ContactBook
        fields = [
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


class ContactBookLabelSerializer(
    serializers.ModelSerializer
):
    contact = serializers.IntegerField(
        help_text="연락처 ID"
    )
    label = serializers.IntegerField(help_text="라벨 ID")

    class Meta:
        model = ContactLabel
        fields = ["contact", "label"]
