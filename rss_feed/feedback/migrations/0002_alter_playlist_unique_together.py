# Generated by Django 4.0.6 on 2023-11-04 04:00

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='playlist',
            unique_together={('account', 'title')},
        ),
    ]
