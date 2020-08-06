from django.shortcuts import render
from .models import Recording, Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .filters import RecordingFilter
from django.db.models import Q
from functools import reduce
from operator import or_


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

  recording_filter = RecordingFilter(response.GET, queryset=recordings)
  recordings = recording_filter.qs
  recordings = recordings.exclude(pk=pk)

  tags = recording.tags.all()

  tags_search = []
  for tag in tags:
    tags_search.append(Q(**{"tags":tag.id}))

  tags_query = reduce(or_, tags_search)
  related_recordings = Recording.objects.filter(tags_query).distinct()
  related_recordings = related_recordings.filter(status="complete").exclude(user=recording.user).exclude(user=response.user)

  context = {
    "view_recording" : recording,
    "recordings" :recordings,
    "recording_filter" :recording_filter,
    "related_recordings" : related_recordings,
  }

  return render(response, 'recordings/view.html', context)
