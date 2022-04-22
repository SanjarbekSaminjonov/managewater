from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.


class Basin(models.Model):

    id = models.CharField(
        max_length=11,
        primary_key=True,
        unique=True,
        verbose_name="qurilma id raqami"
    )

    belong_to = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name='basins',
        verbose_name="foydalanuvchi"
    )

    name = models.CharField(
        max_length=255,
        verbose_name="nomi"
    )

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="latitude",
        blank=True,
        null=True
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="longitude",
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.name} - {self.id}'

    class Meta:
        verbose_name = 'qurilma'
        verbose_name_plural = 'qurilmalar'


class BasinMessage(models.Model):

    basin = models.ForeignKey(
        to=Basin,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name="qurilma"
    )

    h1 = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="qurilma suvdan qancha balandda (santimetr)"
    )

    h2 = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="suv satxidan qancha balandda (santimetr)"
    )

    w1 = models.IntegerField(
        verbose_name="o'tayotgan suv miqdori (litr/sekund)"
    )

    w2 = models.IntegerField(
        verbose_name="o'tayotgan suv miqdori (kub metr/soat)"
    )

    vol = models.DecimalField(
        max_digits=22,
        decimal_places=2,
        verbose_name="jami o'tgan suv miqdori (kub metr)"
    )

    bat = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name="batareya quvvati (volt)"
    )

    net = models.IntegerField(verbose_name="quality")

    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="latitude"
    )

    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name="longitude"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.basin.name

    class Meta:
        verbose_name = 'qurilma ma\'lumoti'
        verbose_name_plural = 'qurilma ma\'lumotlari'
