from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from recordings.models import Recording, RadioStation, Tag
from datetime import date, time, timedelta
from django.utils import timezone
from random import choice

class TestViews(TestCase):

  def setUp(self):
    user = User.objects.create(username='test')
    user.set_password('testpass123')
    user.save()

    radio_station = RadioStation.objects.create(name="BBC One")
    radio_station.save()

    for i in range(0, 3):
      new_recording = Recording.objects.create(
        user           = user,
        radio_station  = radio_station,
        title          = "Title",
        description    = "Description",
        start_datetime = timezone.now() + timedelta(minutes=10),
        end_datetime   = timezone.now() + timedelta(minutes=20),
        status         = choice(["pending", "complete"]),
        public         = choice([False, True, True, True])
      )
      new_recording.save()

    second_user = User.objects.create(username='other')
    second_user.set_password('testpass123')
    second_user.save()


    tag_one = Tag.objects.create(tag="Biochemistry")
    tag_one.save()
    tag_two = Tag.objects.create(tag="Animal")
    tag_two.save()

    recording = Recording.objects.create(
      title          = "New recording",
      user           = user,
      radio_station  = radio_station,
      start_datetime = timezone.now() + timedelta(minutes=10),
      end_datetime   = timezone.now() + timedelta(minutes=20),
      status         = "pending"
      )
    recording.save()
    self.recording       = recording
    self.tag_one         = tag_one
    self.tag_two         = tag_two
    self.date            = date(2021, 7, 1)
    self.start_time      = time(12, 00, 00)
    self.end_time        = time(13, 00, 00)
    self.clientLoggedOut = Client()
    self.clientLoggedIn  = Client()
    self.clientNotAccountOwner = Client()
    self.clientLoggedIn.login(username='test', password='testpass123')
    self.clientNotAccountOwner.login(username='other', password='testpass123')
    self.profile_url      = reverse('profile', args=[user.username])
    self.myrecordings_url = reverse('myrecordings', args=[user.username])
    self.create_url       = reverse('create_recording', args=[user.username])
    self.edit_url         = reverse('myrecording', args=[user.username, recording.id])
    self.settings_url     = reverse('settings', args=[user.username])
    self.listen_url       = reverse('myrecording_listen', args=[user.username, recording.id])
    self.delete_url       = reverse('delete_recording', args=[user.username, recording.id])
    self.radio_station    = radio_station
    self.title            = "This is my title"
    self.public           = 'on'

  # TEST REDIRECTS WHEN LOGGED OUT
  def test_account_view_GET_logged_out(self):
    response = self.clientLoggedOut.get(self.profile_url)
    self.assertEquals(response.status_code, 302)

  def test_my_recordings_view_GET_logged_out(self):
    response = self.clientLoggedOut.get(self.myrecordings_url)
    self.assertEquals(response.status_code, 302)

  def test_settings_view_GET_logged_out(self):
    response = self.clientLoggedOut.get(self.settings_url)
    self.assertEquals(response.status_code, 302)

  def test_create_recording_view_GET_logged_out(self):
    response = self.clientLoggedOut.get(self.create_url)
    self.assertEquals(response.status_code, 302)

  def test_edit_recording_view_GET_logged_out(self):
    response = self.clientLoggedOut.get(self.edit_url)
    self.assertEquals(response.status_code, 302)

  def test_listen_view_GET_logged_out(self):
    response = self.clientLoggedOut.get(self.listen_url)
    self.assertEquals(response.status_code, 302)

  def test_delete_recording_view_GET_logged_out(self):
    recording_count_initial = Recording.objects.count()
    response = self.clientLoggedOut.get(self.delete_url)
    recording_count_final = Recording.objects.count()
    self.assertEquals(response.status_code, 302)
    self.assertEquals(recording_count_initial, recording_count_final)

  # TEST VIEWS GET LOGGED IN
  def test_account_view_GET_logged_in(self):
    response = self.clientLoggedIn.get(self.profile_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/profile.html')

  def test_my_recordings_view_GET_logged_in(self):
    response = self.clientLoggedIn.get(self.myrecordings_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/my_recordings.html')

  def test_settings_view_GET_logged_in(self):
    response = self.clientLoggedIn.get(self.settings_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/settings.html')

  def test_create_recording_view_GET_logged_in(self):
    response = self.clientLoggedIn.get(self.create_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/create.html')

  def test_edit_recording_view_GET_logged_in(self):
    response = self.clientLoggedIn.get(self.edit_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/edit.html')

  def test_listen_view_GET_logged_in(self):
    response = self.clientLoggedIn.get(self.listen_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/listen.html')

  def test_delete_recording_view_GET_logged_in(self):
    recording_count_initial = Recording.objects.count()
    response = self.clientLoggedIn.get(self.delete_url)
    recording_count_final = Recording.objects.count()
    self.assertEquals(recording_count_initial - 1, recording_count_final)
    self.assertEquals(response.status_code, 302)

  # TEST NOT PROFILE USER
  def test_account_view_GET_not_profile_user(self):
    response = self.clientNotAccountOwner.get(self.profile_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/profile.html')

  def test_settings_view_GET_not_profile_user(self):
    response = self.clientNotAccountOwner.get(self.settings_url)
    self.assertEquals(response.status_code, 302)

  def test_my_recordings_view_GET_not_profile_user(self):
    response = self.clientNotAccountOwner.get(self.myrecordings_url)
    self.assertEquals(response.status_code, 302)

  def test_create_recording_view_GET_not_profile_user(self):
    response = self.clientNotAccountOwner.get(self.create_url)
    self.assertEquals(response.status_code, 302)

  def test_edit_recording_view_GET_not_profile_user(self):
    response = self.clientNotAccountOwner.get(self.edit_url)
    self.assertEquals(response.status_code, 302)

  def test_listen_view_GET_not_profile_user(self):
    recording_count_initial = Recording.objects.count()
    response = self.clientNotAccountOwner.get(self.listen_url)
    recording_count_final = Recording.objects.count()
    self.assertEquals(response.status_code, 302)
    self.assertEquals(recording_count_initial, recording_count_final)

  # TEST VIEWS POST LOGGED IN

  # VALID DATA
  def test_account_view_POST(self):
    response = self.clientLoggedIn.post(self.profile_url, {
      "start_date"    : self.date,
      "start_time"    : self.start_time,
      "end_date"      : self.date,
      "end_time"      : self.end_time,
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.assertEquals(response.status_code, 200)
    self.assertEquals(Recording.objects.last().title, self.title)

  def test_create_recording_view_POST(self):
    response = self.clientLoggedIn.post(self.create_url, {
      "start_date"    : self.date,
      "start_time"    : self.start_time,
      "end_date"      : self.date,
      "end_time"      : self.end_time,
      "title"         : "New recording title",
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.assertEquals(response.status_code, 302)
    self.assertEquals(Recording.objects.last().title, "New recording title")

  def test_edit_recording_view_POST(self):
    response = self.clientLoggedIn.post(self.edit_url, {
      "start_date"    : self.date,
      "start_time"    : self.start_time,
      "end_date"      : self.date,
      "end_time"      : self.end_time,
      "title"         : "Edited title",
      "radio_station" : self.radio_station.id,
      "public"        : self.public,
      })
    self.recording = Recording.objects.get(pk=self.recording.id)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(self.recording.title, "Edited title")

  # NO DATA
  def test_account_view_POST_no_data(self):
    recordingCountPre = Recording.objects.all().count()
    response = self.clientLoggedIn.post(self.profile_url)
    recordingCountPost = Recording.objects.all().count()
    self.assertEquals(response.status_code, 200)
    self.assertEquals(recordingCountPre, recordingCountPost)

  def test_create_recording_view_POST_no_data(self):
    recordingCountPre = Recording.objects.all().count()
    response = self.clientLoggedIn.post(self.create_url)
    recordingCountPost = Recording.objects.all().count()
    self.assertEquals(response.status_code, 200)
    self.assertEquals(recordingCountPre, recordingCountPost)

  def test_edit_recording_view_POST_no_data(self):
    recording_title = self.recording.title
    recording_task_id = self.recording.task_id
    response = self.clientLoggedIn.post(self.edit_url)
    self.recording = Recording.objects.get(pk=self.recording.id)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(recording_title, self.recording.title)
    self.assertEquals(recording_task_id, self.recording.task_id)

  # INVALID DATA
  def test_account_view_POST_invalid_data(self):
    recordingCountPre = Recording.objects.all().count()
    response = self.clientLoggedIn.post(self.profile_url, {
      "start_date"    : self.date,
      "start_time"    : self.start_time,
      "end_date"      : self.date,
      "end_time"      : self.end_time,
      "title"         : "",
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    recordingCountPost = Recording.objects.all().count()
    self.assertEquals(response.status_code, 200)
    self.assertEquals(recordingCountPre, recordingCountPost)

  def test_create_recording_view_POST_invalid_data(self):
    recordingCountPre = Recording.objects.all().count()
    response = self.clientLoggedIn.post(self.create_url, {
      "start_date"    : self.date,
      "start_time"    : self.start_time,
      "end_date"      : self.date,
      "end_time"      : self.end_time,
      "title"         : "",
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    recordingCountPost = Recording.objects.all().count()
    self.assertEquals(response.status_code, 200)
    self.assertEquals(recordingCountPre, recordingCountPost)

  def test_edit_recording_view_POST_invalid_data(self):
    recording_title = self.recording.title
    response = self.clientLoggedIn.post(self.edit_url, {
      "start_date"    : self.date,
      "start_time"    : self.start_time,
      "end_date"      : self.date,
      "end_time"      : self.end_time,
      "title"         : "",
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.recording = Recording.objects.get(pk=self.recording.id)
    self.assertEquals(response.status_code, 200)
    self.assertEquals(recording_title, self.recording.title)

  # TEST POST LOGGED OUT
  def test_account_view_POST_logged_out(self):
    recordingCountPre = Recording.objects.all().count()
    response = self.clientLoggedOut.post(self.profile_url, {
      "start_date"    : self.date,
      "start_time"    : self.start_time,
      "end_date"      : self.date,
      "end_time"      : self.end_time,
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    recordingCountPost = Recording.objects.all().count()
    self.assertEquals(recordingCountPre, recordingCountPost)
    self.assertEquals(response.status_code, 302)

  def test_create_recording_view_POST_logged_out(self):
    recordingCountPre = Recording.objects.all().count()
    response = self.clientLoggedOut.post(self.create_url, {
      "start_date"    : self.date,
      "start_time"    : self.start_time,
      "end_date"      : self.date,
      "end_time"      : self.end_time,
      "title"         : self.title,
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    recordingCountPost = Recording.objects.all().count()
    self.assertEquals(recordingCountPre, recordingCountPost)
    self.assertEquals(response.status_code, 302)

  def test_create_recording_view_POST_logged_out(self):
    recording_title = self.recording.title
    response = self.clientLoggedOut.post(self.edit_url, {
      "start_date"    : self.date,
      "start_time"    : self.start_time,
      "end_date"      : self.date,
      "end_time"      : self.end_time,
      "title"         : "Random Title",
      "radio_station" : self.radio_station.id,
      "public"        : self.public
      })
    self.recording = Recording.objects.get(pk=self.recording.id)
    self.assertEquals(recording_title, self.recording.title)
    self.assertEquals(response.status_code, 302)
