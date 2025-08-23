from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class MetaData(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = "Metadata"
        verbose_name_plural = "Metadata"
        ordering = ["key"]


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
