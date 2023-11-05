# Generated by Django 4.0.6 on 2023-11-05 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcast', '0004_rename_itunes_episode_type_episode_itunes_episodetype_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='podcast_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='podcast.owner'),
        ),
        migrations.AlterField(
            model_name='podcast',
            name='podcast_generator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='podcast.generator'),
        ),
    ]