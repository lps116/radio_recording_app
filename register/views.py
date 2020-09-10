from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate

# Create your views here.

# registration form view
# if form is valid, data saved and user signed in and redirected to home page
def registration_view(response):
  form = RegistrationForm()
  if response.method == "POST":
    form = RegistrationForm(response.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(response, user)
      messages.success(response, 'Thank you for signing up with us.')
      return redirect("/")
    else:
      messages.error(response, 'The form is invalid.')

  context = {
    "form" : form
  }
  return render(response, 'register/register.html', context)
