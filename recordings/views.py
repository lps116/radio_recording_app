from django.shortcuts import render
from .models import Recording, Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .filters import RecordingFilter

@login_required(login_url='/login/')
def recordings_index(response):
  recordings = Recording.objects.filter(status="complete", public=True).order_by('-end_datetime')
  popular_tags = Tag.objects.annotate(recordings_count=Count('recordings')).order_by('-recordings_count')[:10]

  recording_filter = RecordingFilter(response.GET, queryset=recordings)
  recordings = recording_filter.qs

  context = {
    "recordings" : recordings,
    "popular_tags" : popular_tags,
    "recording_filter" : recording_filter
  }
  return render(response, 'recordings/index.html', context)

@login_required(login_url='/login/')
def recording_view(response, pk):
  recording = Recording.objects.get(pk=pk)
  recordings = Recording.objects.filter(user=recording.user, status="complete", public=True).order_by('-end_datetime')
  recordings = recordings.exclude(pk=pk)

  recording_filter = RecordingFilter(response.GET, queryset=recordings)
  recordings = recording_filter.qs


  context = {
    "recording" : recording,
    "recordings" :recordings,
    "recording_filter" :recording_filter,
  }
  return render(response, 'recordings/view.html', context)
