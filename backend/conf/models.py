from django.db import models


class CreatedUpdatedHistoryModel(models.Model):
    created_datetime = models.DateTimeField(
        auto_now_add=True, db_comment="생성일시"
    )
    updated_datetime = models.DateTimeField(
        auto_now=True, db_comment="수정일시"
    )

    class Meta:
        abstract = True
