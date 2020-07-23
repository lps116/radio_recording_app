from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .validators import (validate_streaming_url, validate_over_one_character,
validate_title_over_ten_characters, validate_description_over_thirty_characters,
is_mp3_file)
from django.core.exceptions import ValidationError

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

class Tag(models.Model):
  tag = models.CharField(max_length=50,
                         unique=True,
                         blank=False,
                         validators=[validate_over_one_character])

  def __str__(self):
    return self.tag

class Recording(models.Model):
  user               = models.ForeignKey(User,
                                        related_name="recordings",
                                        null=True,
                                        on_delete=models.CASCADE)
  radio_station      = models.ForeignKey(RadioStation,
                                         related_name="recordings",
                                         null=True,
                                         on_delete=models.CASCADE)
  tags               = models.ManyToManyField(Tag, related_name='recordings')
  title              = models.CharField(max_length=50,
                                        null=True,
                                        validators=[validate_title_over_ten_characters])
  description        = models.TextField(max_length=500,
                                        blank=True, null=True,
                                        validators=[validate_description_over_thirty_characters])
  start_datetime     = models.DateTimeField(auto_now=False, auto_now_add=False)
  end_datetime       = models.DateTimeField(auto_now=False, auto_now_add=False)
  requested_datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
  status             = models.CharField(max_length=15,
                                       choices=(
                                        ("pending" , "pending"),
                                        ("in progress", "in progress"),
                                        ("complete", "complete"),
                                        ),
                                       default="pending")
  file                 = models.URLField(max_length=200, blank=True, null=True)
  # file               = models.FileField(upload_to="",
                                        # validators=[is_mp3_file],
                                        # blank=True,
                                        # null=True)
  public             = models.BooleanField(default=True)
  task_id            = models.CharField(max_length=100,
                                        blank = True,
                                        null=True)

  @property
  def time_till_recording(self):
    if self.status == "pending":
      return self.start_datetime - timezone.now()
