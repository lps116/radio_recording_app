from django.shortcuts import render
from .models import Recording
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def recordings_index(response):
  recordings = Recording.objects.filter(status="complete").order_by('-end_datetime')
  context = {
    "recordings" : recordings
  }
  return render(response, 'recordings/index.html', context)

@login_required(login_url='/login/')
def recording_view(response, pk):
  recording = Recording.objects.get(pk=pk)
  context = {
    "recording" : recording
  }
  return render(response, 'recordings/view.html', context)
