from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages


# Create your views here.

def registration_view(response):
  if response.method == "POST":
    form = RegistrationForm(response.POST)
    if form.is_valid():
      form.save()
      messages.success(response, 'Thank you for signing up with us.')
      return redirect("/")
    else:
      messages.error(response, 'The form is invalid.')

  form = RegistrationForm()
  context = {
    "form" : form
  }
  return render(response, 'register/register.html', context)
