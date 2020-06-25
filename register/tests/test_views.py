from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class TestViews(TestCase):

  def setUp(self):
    self.client = Client()
    self.registration_url = reverse('register')

  def test_registration_view_GET(self):
    response = self.client.get(self.registration_url)
    self.assertEquals(response.status_code, 200)
    self.assertTemplateUsed(response, 'register/register.html')

  def test_registration_view_POST(self):
    response = self.client.post(self.registration_url, {
      'first_name' : 'John',
      'last_name'  : 'Smith',
      'username'   : 'john123',
      'email'      : 'john@smith.com',
      'password1'  : 'openplease123',
      'password2'  : 'openplease123'
      })
    self.assertEquals(response.status_code, 302)
    self.assertEquals(User.objects.last().username, 'john123')

  def test_registration_view_POST_no_data(self):
    userCountPre = User.objects.all().count()
    response = self.client.post(self.registration_url)
    userCountPost = User.objects.all().count()
    # double check if 200 is the right response code
    self.assertEquals(response.status_code, 200)
    self.assertEquals(userCountPre, userCountPost)

  def test_registration_view_POST_invalid_data(self):
    userCountPre = User.objects.all().count()
    response = self.client.post(self.registration_url, {
      'first_name' : 'John',
      'last_name'  : 'Smith',
      'username'   : 'john123',
      'email'      : 'john@smith.com',
      'password1'  : 'openplease12345',
      'password2'  : 'openplease123'
      })
    userCountPost = User.objects.all().count()
    # double check if this is the right status
    self.assertEquals(response.status_code, 200)
    self.assertEquals(userCountPre, userCountPost)
