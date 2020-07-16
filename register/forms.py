from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.contrib.auth.forms import AuthenticationForm

class RegistrationForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super(RegistrationForm, self).__init__(*args, **kwargs)
    self.fields['first_name'].widget.attrs = {'class' : 'form-control', 'placeholder': 'John'}
    self.fields['last_name'].widget.attrs = {'class' : 'form-control', 'placeholder': 'Doe'}
    self.fields['username'].widget.attrs = {'class' : 'form-control', 'placeholder': 'john123'}
    self.fields['email'].widget.attrs = {'class' : 'form-control', 'placeholder': 'john@gmail.com'}
    self.fields['password1'].widget.attrs = {'class' : 'form-control', 'placeholder': 'Password'}
    self.fields['password2'].widget.attrs = {'class' : 'form-control', 'placeholder': 'Password'}

  first_name = forms.CharField(max_length=25, required=True)
  last_name  = forms.CharField(max_length=25, required=True)
  email      = forms.EmailField(required=True)

  class Meta:
    model  = User
    fields = ["first_name", "last_name", "username", "email", "password1", "password2"]
