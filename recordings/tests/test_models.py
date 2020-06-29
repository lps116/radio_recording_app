from django.test import TestCase
from django.contrib.auth.models import User
from recordings.models import Recording, RadioStation
from django.utils import timezone
from datetime import timedelta


class TestModels(TestCase):

  def setUp(self):
    start_time = timezone.now() + timedelta(days = 1)
    end_time  = timezone.now() + timedelta(days = 1, minutes=30)

    user = User.objects.create(username='test')
    user.set_password('testuser123')
    user.save()

    radio_station = RadioStation.objects.create(name = 'Test station')
    radio_station.save()

    recording = Recording.objects.create(
      title  = 'Test',
      user = user,
      radio_station = radio_station,
      start_datetime = start_time,
      end_datetime = end_time,
      )
    recording.save()

    self.recording = recording
    self.start_time = start_time
    self.end_time = end_time

  def test_time_till_recording_valid_state(self):
    time_until_method = self.recording.time_till_recording
    time_until_calc   = self.start_time - timezone.now()
    self.assertEquals(time_until_method.seconds, time_until_calc.seconds)

  def test_time_till_recording_invalid_state(self):
    self.recording.status = "complete"
    self.recording.save()
    time_until_method = self.recording.time_till_recording
    self.assertEquals(time_until_method, None)



