from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account.views import account_view

class TestUrls(SimpleTestCase):

  def test_account_view_url_is_resolved(self):
    url = reverse('profile', args=['user123'])
    self.assertEquals(resolve(url).func, account_view)

