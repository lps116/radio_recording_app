# Generated by Django 3.0.7 on 2020-07-23 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0012_auto_20200720_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='file',
            field=models.URLField(blank=True, null=True),
        ),
    ]