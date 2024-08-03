from django.contrib.auth.models import User
from django.db import models

from conf.models import (
    CreatedUpdatedHistoryModel,
    CustomManager,
)


class Label(CreatedUpdatedHistoryModel):
    owner = models.ForeignKey(
        User,
        related_name="label",
        on_delete=models.CASCADE,
        db_comment="주소록 소유자",
    )
    name = models.CharField(
        max_length=50, db_comment="라벨 이름"
    )

    objects = CustomManager()

    class Meta:
        db_table = "label"
        db_table_comment = "라벨"
