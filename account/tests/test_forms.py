from django.test import TestCase
from account.forms import CreateRecordingForm
from recordings.models import RadioStation
from datetime import date, time, datetime, timedelta

class TestForms(TestCase):

  def setUp(self):
    radio_station = RadioStation.objects.create(name = "BBC Two")
    radio_station.save()
    self.radio_station = radio_station

  def test_create_recording_form(self):
    form = CreateRecordingForm(data={
      "start_date"    : date.today(),
      "start_time"    : (datetime.now() + timedelta(minutes=20)).time(),
      "end_date"      : date.today(),
      "end_time"      : (datetime.now() + timedelta(minutes=30)).time(),
      "title"         : "This is my title",
      "radio_station" : self.radio_station.id,
      "public"        : 'on'
      })
    self.assertTrue(form.is_valid())

  def test_create_recording_no_data(self):
    form = CreateRecordingForm(data={})
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 6)


  def test_create_form_early_start_date(self):
    form = CreateRecordingForm(data={
      "start_date"    : date.today(),
      "start_time"    : (datetime.now() + timedelta(minutes=0)).time(),
      "end_date"      : date.today(),
      "end_time"      : (datetime.now() + timedelta(minutes=30)).time(),
      "title"         : "This is my title",
      "radio_station" : self.radio_station.id,
      "public"        : 'on'
      })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)

  def test_create_form_recording_too_long(self):
    form = CreateRecordingForm(data={
      "start_date"    : date.today(),
      "start_time"    : (datetime.now() + timedelta(minutes=20)).time(),
      "end_date"      : date.today(),
      "end_time"      : (datetime.now() + timedelta(minutes=300)).time(),
      "title"         : "This is my title",
      "radio_station" : self.radio_station.id,
      "public"        : 'on'
      })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)

  def test_create_form_recording_end_date_before_start(self):
    form = CreateRecordingForm(data={
      "start_date"    : date.today(),
      "start_time"    : (datetime.now() + timedelta(minutes=40)).time(),
      "end_date"      : date.today(),
      "end_time"      : (datetime.now() + timedelta(minutes=20)).time(),
      "title"         : "This is my title",
      "radio_station" : self.radio_station.id,
      "public"        : 'on'
      })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)
