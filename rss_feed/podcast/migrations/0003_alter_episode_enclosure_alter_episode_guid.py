# Generated by Django 4.0.6 on 2023-10-11 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0002_alter_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='enclosure',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='episode',
            name='guid',
            field=models.CharField(max_length=150),
        ),
    ]
