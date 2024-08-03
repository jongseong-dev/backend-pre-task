from django.contrib.auth.models import User
from django.db import models

from conf.models import CreatedUpdatedHistoryModel
from label.models import Label


class ContactBook(CreatedUpdatedHistoryModel):
    owner = models.ForeignKey(
        User,
        related_name="contact_book",
        on_delete=models.CASCADE,
        db_comment="주소록 소유자",
    )
    name = models.CharField(
        max_length=50, db_comment="저장한 이름"
    )
    email = models.EmailField(db_comment="저장한 이메일")
    phone = models.CharField(
        max_length=20, db_comment="저장한 전화번호"
    )
    company = models.CharField(
        max_length=50, blank=True, db_comment="저장한 회사"
    )
    position = models.CharField(
        max_length=50, blank=True, db_comment="저장한 직책"
    )
    memo = models.TextField(blank=True, db_comment="메모")
    profile_image_url = models.URLField(
        blank=True, db_comment="프로필 이미지 URL"
    )
    address = models.CharField(
        max_length=100, blank=True, db_comment="주소"
    )
    birthday = models.DateTimeField(
        blank=True, null=True, db_comment="생일"
    )
    website_url = models.URLField(
        blank=True, db_comment="웹사이트 URL"
    )

    class Meta:
        db_table = "contactbook"
        db_table_comment = "주소록"
        indexes = [models.Index(fields=["name"])]


class ContactLabel(CreatedUpdatedHistoryModel):
    contact = models.ForeignKey(
        ContactBook,
        related_name="labeled_contact",
        on_delete=models.CASCADE,
        db_comment="주소록",
    )
    label = models.ForeignKey(
        Label,
        related_name="labeled_contact",
        on_delete=models.CASCADE,
        db_comment="라벨",
    )

    class Meta:
        db_table = "contactbook_label"
        db_table_comment = "주소록에 있는 연락처의 라벨링을 관리하는 테이블"
