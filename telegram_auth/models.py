from django.db import models
from django.conf import settings


class TelegramToken(models.Model):
    token = models.CharField(max_length=32)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
