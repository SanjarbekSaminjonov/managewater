# Generated by Django 4.0.4 on 2022-04-22 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basin',
            fields=[
                ('id', models.CharField(max_length=11, primary_key=True, serialize=False, unique=True, verbose_name='qurilma id raqami')),
                ('phone', models.CharField(max_length=15, verbose_name='telefon raqam')),
                ('name', models.CharField(max_length=255, verbose_name='nomi')),
                ('height', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='qurilma suv tubidan balandligi (santimetr)')),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='latitude')),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True, verbose_name='longitude')),
            ],
            options={
                'verbose_name': 'qurilma',
                'verbose_name_plural': 'qurilmalar',
            },
        ),
        migrations.CreateModel(
            name='BasinMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('h1', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='qurilma suvdan qancha balandda (santimetr)')),
                ('h2', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='suv satxidan qancha balandda (santimetr)')),
                ('w1', models.IntegerField(verbose_name="o'tayotgan suv miqdori (litr/sekund)")),
                ('w2', models.IntegerField(verbose_name="o'tayotgan suv miqdori (kub metr/soat)")),
                ('vol', models.DecimalField(decimal_places=2, max_digits=22, verbose_name="jami o'tgan suv miqdori (kub metr)")),
                ('bat', models.DecimalField(decimal_places=2, max_digits=4, verbose_name='batareya quvvati (volt)')),
                ('net', models.IntegerField(verbose_name='quality')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='latitude')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='longitude')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('basin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='basins.basin', verbose_name='qurilma')),
            ],
            options={
                'verbose_name': "qurilma ma'lumoti",
                'verbose_name_plural': "qurilma ma'lumotlari",
            },
        ),
    ]
