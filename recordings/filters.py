import django_filters
from .models import Recording

class RecordingFilter(django_filters.FilterSet):
  class Meta:
    model = Recording
    fields = ['tags', 'radio_station']
