# Generated by Django 4.0.4 on 2022-05-16 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basins', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basin',
            name='conf_height',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
