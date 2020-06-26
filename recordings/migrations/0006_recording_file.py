# Generated by Django 3.0.7 on 2020-06-26 16:56

from django.db import migrations, models
import recordings.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0005_auto_20200626_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='recording',
            name='file',
            field=models.FileField(blank=True, upload_to='media/recordings', validators=[recordings.validators.is_mp3_file]),
        ),
    ]
