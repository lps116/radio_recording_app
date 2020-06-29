from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from recordings.models import RadioStation, Recording
from django.utils import timezone
from datetime import timedelta

class TestViews(TestCase):

  def setUp(self):
    user = User.objects.create(username='test')
    user.set_password('testpass123')
    user.save()
    radio_station = RadioStation.objects.create(name='Test station')
    radio_station.save()
    recording = Recording.objects.create(title='This is a test recording',
                                         user = user,
                                         radio_station = radio_station,
                                         start_datetime = timezone.now() + timedelta(days=1),
                                         end_datetime = timezone.now() + timedelta(days=1, minutes=30),
                                         status = 'pending')
    recording.save()
    self.clientLoggedOut = Client()
    self.clientLoggedIn = Client()
    self.clientLoggedIn.login(username='test', password='testpass123')
    self.recordings_url = reverse('recordings')
    self.recording_url  = reverse('recording', args=[recording.id])


  def test_recordings_index_GET_logged_out(self):
    response = self.clientLoggedOut.get(self.recordings_url)
    self.assertEquals(response.status_code, 302)

  def test_recordings_index_GET_logged_in(self):
    response = self.clientLoggedIn.get(self.recordings_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'recordings/index.html')

  def test_recrding_view_GET_logged_out(self):
    response = self.clientLoggedOut.get(self.recording_url)
    self.assertEquals(response.status_code, 302)

  def test_recording_view_GET_logged_in(self):
    response = self.clientLoggedIn.get(self.recording_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'recordings/view.html')
