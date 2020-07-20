from django.urls import path
from . import views

urlpatterns = [
  path('', views.account_view, name='profile'),
  path('myrecordings/', views.recordings_view, name='myrecordings'),
  path('settings/', views.settings_view, name='settings'),
  path('myrecordings/<int:recording_id>/', views.edit_view, name='myrecording'),
  path('myrecordings/<int:recording_id>/delete/', views.delete_view, name='delete_recording'),
  path('myrecordings/create/', views.create_view, name='create_recording'),
]
