from django.test import SimpleTestCase
from django.urls import reverse, resolve
from home.views import home_view

class TestUrls(SimpleTestCase):
  # make sure right view loaded
  def test_home_url_is_resolved(self):
    url = reverse('home')
    self.assertEquals(resolve(url).func, home_view)
