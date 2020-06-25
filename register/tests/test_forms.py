from django.test import TestCase
from register.forms import RegistrationForm


class TestForms(TestCase):

  def test_registration_form_valid_data(self):
    form = RegistrationForm(data={
      'first_name' : 'John',
      'last_name'  : 'Smith',
      'username'   : 'john123',
      'email'      : 'john@smith.com',
      'password1'  : 'openplease123',
      'password2'  : 'openplease123'
      })
    self.assertTrue(form.is_valid())

  def test_registration_form_no_data(self):
    form = RegistrationForm(data={})
    self.assertFalse(form.is_valid())
    self.assertEquals(len(form.errors), 6)
