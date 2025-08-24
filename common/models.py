from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class MetaData(models.Model):
    key = models.CharField(max_length=100)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        ordering = [
            "key",
        ]
        constraints = [
            models.UniqueConstraint(fields=["key", "value"], name="unique_key_value")
        ]

        indexes = [
            models.Index(fields=["key", "value"]),
        ]
