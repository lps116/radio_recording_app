from django.test import SimpleTestCase
from django.urls import reverse, resolve
from recordings.views import recordings_index, recording_view

class TestUrls(SimpleTestCase):

  # check that urls call the right view methods
  def test_recordings_url_is_resolved(self):
    url = reverse('recordings')
    self.assertEquals(resolve(url).func, recordings_index)

  def test_recording_view_url_is_resolved(self):
    url = reverse('recording', args=[1])
    self.assertEquals(resolve(url).func, recording_view)
