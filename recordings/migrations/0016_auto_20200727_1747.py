# Generated by Django 3.0.7 on 2020-07-27 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0015_auto_20200727_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='recordings', to='recordings.Tag'),
        ),
    ]
