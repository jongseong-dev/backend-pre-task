from django.contrib.auth.models import User
from django.db import models

from apps.consts import ManagerChoices
from apps.models import (
    CreatedUpdatedHistoryModel,
    get_model_manager,
)


class Label(CreatedUpdatedHistoryModel):
    owner = models.ForeignKey(
        User,
        related_name="label",
        on_delete=models.CASCADE,
        db_comment="주소록 소유자",
    )
    name = models.CharField(max_length=50, db_comment="라벨 이름")

    objects = get_model_manager(ManagerChoices.CUSTOM)

    class Meta:
        db_table = "label"
        db_table_comment = "라벨"
