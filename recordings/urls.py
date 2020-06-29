from django.urls import path
from . import views

urlpatterns = [
  path('', views.recordings_index, name='recordings'),
  path('<int:pk>/', views.recording_view, name='recording')
]
