from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from recordings.models import Recording, RadioStation
from datetime import date, time

class TestViews(TestCase):

  def setUp(self):
    user = User.objects.create(username='test')
    user.set_password('testpass123')
    user.save()

    radio_station = RadioStation.objects.create(name="BBC One")
    radio_station.save()
    self.clientLoggedOut = Client()
    self.clientLoggedIn = Client()
    self.clientLoggedIn.login(username='test', password='testpass123')
    self.profile_url  = reverse('profile', args=[user.username])
    self.radio_station = radio_station

  def test_account_view_GET_logged_out(self):
    response = self.clientLoggedOut.get(self.profile_url)
    self.assertEquals(response.status_code, 302)

  def test_account_view_GET_logged_in(self):
    response = self.clientLoggedIn.get(self.profile_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'account/profile.html')

  def test_account_view_POST(self):
    response = self.clientLoggedIn.post(self.profile_url, {
      "start_date"    : date(2021, 7, 1),
      "start_time"    : time(12, 00, 00),
      "end_date"      : date(2021, 7, 1),
      "end_time"      : time(13, 00, 00),
      "title"         : "This is my title",
      "radio_station" : self.radio_station.id,
      "public"        : 'on'
      })
    self.assertEquals(response.status_code, 200)
    self.assertEquals(Recording.objects.last().title, 'This is my title')

  def test_account_view_POST_no_data(self):
    recordingCountPre = Recording.objects.all().count()
    response = self.clientLoggedIn.post(self.profile_url)
    recordingCountPost = Recording.objects.all().count()
    self.assertEquals(response.status_code, 200)
    self.assertEquals(recordingCountPre, recordingCountPost)

  def test_account_view_POST_invalid_data(self):
    recordingCountPre = Recording.objects.all().count()
    response = self.clientLoggedIn.post(self.profile_url, {
      "start_date"    : date(2021, 7, 1),
      "start_time"    : time(12, 00, 00),
      "end_date"      : date(2021, 7, 1),
      "end_time"      : time(13, 00, 00),
      "title"         : "",
      "radio_station" : self.radio_station.id,
      "public"        : 'on'
      })
    recordingCountPost = Recording.objects.all().count()
    self.assertEquals(response.status_code, 200)
    self.assertEquals(recordingCountPre, recordingCountPost)

  def test_account_view_POST_logged_out(self):
    recordingCountPre = Recording.objects.all().count()
    response = self.clientLoggedOut.post(self.profile_url, {
      "start_date"    : date(2021, 7, 1),
      "start_time"    : time(12, 00, 00),
      "end_date"      : date(2021, 7, 1),
      "end_time"      : time(13, 00, 00),
      "title"         : "This is my title",
      "radio_station" : self.radio_station.id,
      "public"        : 'on'
      })
    recordingCountPost = Recording.objects.all().count()
    self.assertEquals(recordingCountPre, recordingCountPost)
    self.assertEquals(response.status_code, 302)
