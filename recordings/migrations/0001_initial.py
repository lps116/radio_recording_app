# Generated by Django 3.0.7 on 2020-06-26 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RadioStation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('streaming_link', models.URLField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recording',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('requested_datetime', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pen', 'pending'), ('inprog', 'in progress'), ('comp', 'complete')], default='pen', max_length=15)),
                ('radio_station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recordings', to='recordings.RadioStation')),
                ('tags', models.ManyToManyField(related_name='recordings', to='recordings.Tag')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recordings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
