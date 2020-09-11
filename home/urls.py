from django.urls import path
from . import views

urlpatterns = [
  # path to homepage
  path('', views.home_view, name='home'),
]
