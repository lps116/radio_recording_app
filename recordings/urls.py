from django.urls import path
from . import views

urlpatterns = [
  # path to /recordings/
  path('', views.recordings_index, name='recordings'),
  # path to /recordings/pk
  path('<int:pk>/', views.recording_view, name='recording')
]
