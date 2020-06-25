from django.shortcuts import render

def home_view(response):
  return render(response, 'home/home.html', {})
