# Generated by Django 3.0.7 on 2020-06-29 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0008_auto_20200626_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]