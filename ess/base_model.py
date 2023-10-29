import uuid

from django.utils import timezone
from django.db import models


class BaseModelClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, db_index=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, db_index=True)

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
