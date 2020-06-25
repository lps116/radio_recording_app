from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
  first_name = forms.CharField(max_length=25, required=True)
  last_name  = forms.CharField(max_length=25, required=True)
  email      = forms.EmailField(required=True)

  class Meta:
    model  = User
    fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
