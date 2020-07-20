from django.urls import path
from . import views

urlpatterns = [
  path('', views.account_view, name='profile'),
  path('myrecordings/', views.recordings_view, name='myrecordings'),
  path('settings/', views.settings_view, name='settings'),
  path('myrecordings/<int:recording_id>/', views.edit_view, name='myrecording'),
  path('myrecording/<int:recording_id>/delete', views.delete_view, name='delete_recording')
]
