from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .validators import (validate_streaming_url, validate_over_one_character,
validate_title_over_ten_characters, validate_description_over_thirty_characters,
is_mp3_file)
from django.core.exceptions import ValidationError
# defining models used in website

# defining radio station model
class RadioStation(models.Model):
  name           = models.CharField(max_length=100,
                                    unique=True,
                                    blank=False,
                                    validators=[validate_over_one_character])
  streaming_link = models.URLField(max_length=300,
                                   null=True,
                                   blank=True,
                                   validators=[validate_streaming_url])

  def __str__(self):
    return self.name

# defining tag model
class Tag(models.Model):
  tag = models.CharField(max_length=50,
                         unique=True,
                         blank=False,
                         validators=[validate_over_one_character])

  def __str__(self):
    return self.tag

# defining recording model
class Recording(models.Model):
  # delete user recrodings if user deleted
  user               = models.ForeignKey(User,
                                        related_name="recordings",
                                        null=True,
                                        on_delete=models.CASCADE)
  # delete recording of station if radio station deleted
  radio_station      = models.ForeignKey(RadioStation,
                                         related_name="recordings",
                                         null=True,
                                         on_delete=models.CASCADE)
  # defining many to many relationship with tags
  tags               = models.ManyToManyField(Tag,
                                              related_name='recordings',
                                              blank=True)
  title              = models.CharField(max_length=50,
                                        null=True,
                                        validators=[validate_over_one_character])
  description        = models.TextField(max_length=500,
                                        blank=True, null=True,
                                        validators=[validate_over_one_character])
  start_datetime     = models.DateTimeField(auto_now=False, auto_now_add=False)
  end_datetime       = models.DateTimeField(auto_now=False, auto_now_add=False)
  requested_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
  # only four valid statuses
  status             = models.CharField(max_length=15,
                                       choices=(
                                        ("pending" , "pending"),
                                        ("in progress", "in progress"),
                                        ("complete", "complete"),
                                        ("failed", "failed")
                                        ),
                                       default="pending")
  file               = models.URLField(max_length=200, blank=True, null=True)
  public             = models.BooleanField(default=True)
  # task_id refers to the id of recroding task in celery queue
  task_id            = models.CharField(max_length=100,
                                        blank = True,
                                        null=True)
  # caluculate time till recording method
  @property
  def time_till_recording(self):
    if self.status == "pending":
      return self.start_datetime - timezone.now()
