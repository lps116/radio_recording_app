from django.test import TestCase
from account.forms import CreateRecordingForm, EditRecordingFormComplete, EditRecordingFormPending
from recordings.models import RadioStation, Tag
from datetime import date, time, datetime, timedelta

class TestForms(TestCase):

  def setUp(self):
    radio_station = RadioStation.objects.create(name = "BBC Two")
    tag           = Tag.objects.create(tag = "Biology")
    tag_two       = Tag.objects.create(tag = "Animals")
    radio_station.save()
    tag.save()
    tag_two.save()
    self.radio_station     = radio_station
    self.tag_one           = tag
    self.tag_two           = tag_two
    self.date              = date.today()
    self.valid_start_time  = (datetime.now() + timedelta(minutes=20)).time()
    self.valid_end_time    = (datetime.now() + timedelta(minutes=30)).time()
    self.title             = "This is a title"
    self.description       = "This is a description"
    self.public            = 'on'

  # TEST FORMS WITH VALID DATA
  def test_create_recording_form(self):
    form = CreateRecordingForm(data={
      "start_date"    : self.date,
      "start_time"    : self.valid_start_time,
      "end_date"      : self.date,
      "end_time"      : self.valid_end_time,
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.assertTrue(form.is_valid())

  def test_edit_recording_pending_form(self):
    form = EditRecordingFormPending(data={
      "start_date"    : self.date,
      "start_time"    : self.valid_start_time,
      "end_date"      : self.date,
      "end_time"      : self.valid_end_time,
      "description"   : self.description,
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public,
      "tags"          : [self.tag_one, self.tag_two],
      })
    self.assertTrue(form.is_valid())

  def test_edit_recording_complete_form(self):
    form = EditRecordingFormComplete(data={
      "description"   : self.description,
      "title"         : self.title,
      "public"        : self.public,
      "tags"          : [self.tag_one, self.tag_two],
      })
    self.assertTrue(form.is_valid())

  # TEST FAILURE OF EMPTY FORM
  def test_create_recording_no_data(self):
    form = CreateRecordingForm(data={})
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 6)

  def test_edit_recording_pending_form_no_data(self):
    form = EditRecordingFormPending(data={})
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 6)

  def test_edit_recording_complete_form_no_data(self):
    form = EditRecordingFormComplete(data={})
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)

  # TEST FORMS INCORRECT TIMES
  def test_create_form_early_start_date(self):
    form = CreateRecordingForm(data={
      "start_date"    : self.date,
      "start_time"    : (datetime.now() + timedelta(minutes=0)).time(),
      "end_date"      : self.date,
      "end_time"      : (datetime.now() + timedelta(minutes=30)).time(),
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)

  def test_edit_pending_form_early_start_date(self):
    form = EditRecordingFormPending(data={
      "start_date"    : self.date,
      "start_time"    : (datetime.now() + timedelta(minutes=0)).time(),
      "end_date"      : self.date,
      "end_time"      : (datetime.now() + timedelta(minutes=30)).time(),
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)

  # TEST FORMS RECORDING LENGTH EXCEEDED
  def test_create_form_recording_too_long(self):
    form = CreateRecordingForm(data={
      "start_date"    : self.date,
      "start_time"    : (datetime.now() + timedelta(minutes=20)).time(),
      "end_date"      : self.date,
      "end_time"      : (datetime.now() + timedelta(minutes=300)).time(),
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)

  def test_edit_pending_form_recording_too_long(self):
    form = EditRecordingFormPending(data={
      "start_date"    : self.date,
      "start_time"    : (datetime.now() + timedelta(minutes=20)).time(),
      "end_date"      : self.date,
      "end_time"      : (datetime.now() + timedelta(minutes=300)).time(),
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)

  # TEST FORMS RECORIDNG TIME TOO EARLY
  def test_create_form_recording_end_date_before_start(self):
    form = CreateRecordingForm(data={
      "start_date"    : self.date,
      "start_time"    : (datetime.now() + timedelta(minutes=40)).time(),
      "end_date"      : self.date,
      "end_time"      : (datetime.now() + timedelta(minutes=20)).time(),
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)

  def test_edit_pending_form_recording_end_date_before_start(self):
    form = CreateRecordingForm(data={
      "start_date"    : self.date,
      "start_time"    : (datetime.now() + timedelta(minutes=40)).time(),
      "end_date"      : self.date,
      "end_time"      : (datetime.now() + timedelta(minutes=20)).time(),
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 1)
