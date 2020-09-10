import django_filters
from .models import Recording

# filter class which filters Recording models
# based on tags and radio stations
class RecordingFilter(django_filters.FilterSet):
  class Meta:
    model = Recording
    fields = ['tags', 'radio_station']
