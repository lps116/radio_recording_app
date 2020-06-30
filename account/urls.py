from django.urls import path
from . import views

urlpatterns = [
  path('<slug:username>/', views.account_view, name='profile'),
]
