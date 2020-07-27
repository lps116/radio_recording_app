from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account.views import account_view, recordings_view, settings_view, edit_view, delete_view, create_view, listen_view

class TestUrls(SimpleTestCase):

  def test_account_view_url_is_resolved(self):
    url = reverse('profile', args=['user123'])
    self.assertEquals(resolve(url).func, account_view)

  def test_my_recordings_url_is_resolved(self):
    url = reverse('myrecordings', args=['user123'])
    self.assertEquals(resolve(url).func, recordings_view)

  def test_settings_url_is_resolved(self):
    url = reverse('settings', args=['user123'])
    self.assertEquals(resolve(url).func, settings_view)

  def test_edit_url_is_resolved(self):
    url = reverse('myrecording', args=['user123', 1])
    self.assertEquals(resolve(url).func, edit_view)

  def test_delete_url_is_resolved(self):
    url = reverse('delete_recording', args=['user123', 1])
    self.assertEquals(resolve(url).func, delete_view)

  def test_create_url_is_resolved(self):
    url = reverse('create_recording', args=['user123'])
    self.assertEquals(resolve(url).func, create_view)

  def test_listen_url_is_resolved(self):
    url = reverse('myrecording_listen', args=['user123', 1])
    self.assertEquals(resolve(url).func, listen_view)
