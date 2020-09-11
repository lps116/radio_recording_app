from django.shortcuts import render

# no context loaded for homepage view
# simply render template
def home_view(response):
  return render(response, 'home/home.html', {})
