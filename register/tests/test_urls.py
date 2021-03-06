from django.test import SimpleTestCase
from django.urls import reverse, resolve
from register.views import registration_view


class TestUrls(SimpleTestCase):

  # check that /register/ url calls registration_view
  def test_registration_url_is_resolved(self):
    url = reverse('register')
    self.assertEquals(resolve(url).func, registration_view)
