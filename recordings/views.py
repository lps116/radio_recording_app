from django.shortcuts import render
from .models import Recording, Tag
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .filters import RecordingFilter
from django.db.models import Q
from functools import reduce
from operator import or_

# view only accessible to user if logged in.
# view for public recordings page
@login_required(login_url='/login/')
def recordings_index(response):
  recordings = Recording.objects.filter(status="complete", public=True).order_by('-end_datetime')
  popular_tags = Tag.objects.annotate(recordings_count=Count('recordings')).order_by('-recordings_count')[:10]
  # create filter object based on user filter selection
  recording_filter = RecordingFilter(response.GET, queryset=recordings)
  # apply filter to the recording list
  recordings = recording_filter.qs

  context = {
    "recordings" : recordings,
    "popular_tags" : popular_tags,
    "recording_filter" : recording_filter
  }
  return render(response, 'recordings/index.html', context)

# view for page to listen to recordings
# context includes recording, other recordings by same user (filtered) and
# list of related recordings (based on similar tags)
@login_required(login_url='/login/')
def recording_view(response, pk):
  # recording requested to listen to
  recording = Recording.objects.get(pk=pk)
  # other recordings by user
  recordings = Recording.objects.filter(user=recording.user, status="complete", public=True).order_by('-end_datetime')

  # filter other recrodings by user
  recording_filter = RecordingFilter(response.GET, queryset=recordings)
  recordings = recording_filter.qs
  recordings = recordings.exclude(pk=pk)

  tags = recording.tags.all()
  # find recordings with similar tags to requested recording
  if tags:
    tags_search = []
    for tag in tags:
      tags_search.append(Q(**{"tags":tag.id}))
      tags_query = reduce(or_, tags_search)
      related_recordings = Recording.objects.filter(tags_query).distinct()
      related_recordings = related_recordings.filter(status="complete").exclude(user=recording.user).exclude(user=response.user)
  else:
    related_recordings = None

  context = {
    "view_recording" : recording,
    "recordings" :recordings,
    "recording_filter" :recording_filter,
    "related_recordings" : related_recordings,
  }

  return render(response, 'recordings/view.html', context)
