# Generated by Django 4.2.3 on 2023-09-18 22:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(blank=True, max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('parent_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcast.category')),
            ],
        ),
        migrations.CreateModel(
            name='Enclosure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('length', models.PositiveIntegerField(blank=True, null=True)),
                ('c_type', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Generator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hostname', models.CharField(blank=True, max_length=150, null=True)),
                ('genDate', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basemodel')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('language', models.CharField(max_length=50)),
                ('explicit', models.CharField(max_length=50)),
                ('itunes_type', models.CharField(blank=True, max_length=50, null=True)),
                ('copy_right', models.CharField(blank=True, max_length=100, null=True)),
                ('pubDate', models.DateTimeField(blank=True, null=True)),
                ('last_build_date', models.DateTimeField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('itunes_subtitle', models.TextField(blank=True, null=True)),
                ('itunes_keywords', models.TextField(blank=True, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='podcast.author')),
                ('category', models.ManyToManyField(to='podcast.category')),
                ('generator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='podcast.generator')),
                ('image', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='podcast.image')),
            ],
            bases=('core.basemodel',),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('guid', models.CharField(blank=True, max_length=400, null=True)),
                ('itunes_duration', models.CharField(blank=True, max_length=50, null=True)),
                ('itunes_episode_type', models.CharField(blank=True, max_length=50, null=True)),
                ('itunes_explicit', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(blank=True, null=True)),
                ('itunes_keywords', models.TextField(blank=True, null=True)),
                ('itunes_player', models.CharField(blank=True, max_length=50, null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='podcast.author')),
                ('enclosure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcast.enclosure')),
                ('episode_podcast', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='podcast.podcast')),
            ],
        ),
    ]
