from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def account_view(response, username):
  user = User.objects.get(username=username)
  scheduled_recordings = user.recordings.filter(status="pending")
  completed_recordings = user.recordings.filter(status="complete")
  inprogress_recordings = user.recordings.filter(status="in progress")
  context = {
    "user" : user,
    "scheduled_recordings": scheduled_recordings,
    "completed_recordings" : completed_recordings,
    "inprogress_recordings" : inprogress_recordings
  }
  return render(response, 'account/profile.html', context)
