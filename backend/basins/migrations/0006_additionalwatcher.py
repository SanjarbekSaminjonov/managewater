# Generated by Django 4.0.4 on 2022-05-27 17:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basins', '0005_alter_basinid_options_alter_basinid_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalWatcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basins.basin')),
                ('watcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]