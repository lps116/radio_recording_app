# Generated by Django 3.0.7 on 2020-06-26 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0004_auto_20200626_1235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recording',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('in progress', 'in progress'), ('complete', 'complete')], default='pending', max_length=15),
        ),
    ]
