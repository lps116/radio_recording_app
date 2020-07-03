from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import CreateRecordingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from recordings.models import Recording, RadioStation
from datetime import datetime
import pytz

# Create your views here.
@login_required(login_url='/login/')
def account_view(response, username):
  if response.method == "POST":
    form = CreateRecordingForm(response.POST)
    if form.is_valid():
      title = form.cleaned_data['title']
      radio_station = form.cleaned_data['radio_station']
      public = form.cleaned_data['public']
      user = response.user
      start_datetime = datetime.combine(form.cleaned_data['start_date'],
                                        form.cleaned_data['start_time'])
      end_datetime = datetime.combine(form.cleaned_data['end_date'],
                                      form.cleaned_data['end_time'])

      timezone = pytz.timezone("Europe/London")
      start_datetime_aware = timezone.localize(start_datetime)
      end_datetime_aware = timezone.localize(end_datetime)
      recording = Recording.objects.create(
        user           = user,
        title          = title,
        radio_station  = radio_station,
        public         = public,
        start_datetime = start_datetime_aware,
        end_datetime   = end_datetime_aware
        )

      recording.save()
      string = "Your " + radio_station.name + " recording has been scheduled."
      messages.success(response, "Your recording has been scheduled.")

  form = CreateRecordingForm()
  user = User.objects.get(username=username)
  scheduled_recordings = user.recordings.filter(status="pending").order_by('start_datetime')
  completed_recordings = user.recordings.filter(status="complete").order_by('-end_datetime')
  inprogress_recordings = user.recordings.filter(status="in progress").order_by('start_datetime')
  context = {
        "user" : user,
        "scheduled_recordings"  : scheduled_recordings,
        "completed_recordings"  : completed_recordings,
        "inprogress_recordings" : inprogress_recordings,
        }
  if user == response.user:
    context["form"] = form
    return render(response, 'account/profile.html', context)
  else:
    return render(response, 'account/profile.html', context)
