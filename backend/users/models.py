from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    phone = models.CharField(
        max_length=255,
        verbose_name="telefon raqam"
    )
    region = models.CharField(max_length=255, verbose_name="viloyat/shahar")
    city = models.CharField(max_length=255, verbose_name="shahar/tuman")
    org_name = models.CharField(max_length=500, verbose_name="tashkilot nomi")
    chat_id = models.CharField(
        max_length=255,
        verbose_name="Telegram id",
        null=True
    )

    class Meta:
        verbose_name = "foydalanuvchi"
        verbose_name_plural = "foydalanuvchilar"
