# Generated by Django 3.0.7 on 2020-06-26 12:35

from django.db import migrations, models
import recordings.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recordings', '0003_auto_20200626_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radiostation',
            name='name',
            field=models.CharField(max_length=100, unique=True, validators=[recordings.validators.validate_over_one_character]),
        ),
        migrations.AlterField(
            model_name='recording',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True, validators=[recordings.validators.validate_description_over_thirty_characters]),
        ),
        migrations.AlterField(
            model_name='recording',
            name='title',
            field=models.CharField(max_length=50, null=True, validators=[recordings.validators.validate_title_over_ten_characters]),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(max_length=50, unique=True, validators=[recordings.validators.validate_over_one_character]),
        ),
    ]