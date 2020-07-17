from django.urls import path
from . import views

urlpatterns = [
  path('', views.account_view, name='profile'),
  path('myrecordings/', views.recordings_view, name='myrecordings'),
  path('settings/', views.settings_view, name='settings')
]
