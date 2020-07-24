from django.urls import path
from . import views

urlpatterns = [
  path('', views.account_view, name='profile'),
  path('myrecordings/', views.recordings_view, name='myrecordings'),
  path('settings/', views.settings_view, name='settings'),
  path('myrecordings/<int:recording_id>/edit/', views.edit_view, name='myrecording'),
  path('myrecordings/<int:recording_id>/delete/', views.delete_view, name='delete_recording'),
  path('myrecordings/create/', views.create_view, name='create_recording'),
  path('myrecordings/<int:recording_id>/view/', views.listen_view, name='myrecording_listen')
]
