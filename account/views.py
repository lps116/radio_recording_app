from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CreateRecordingForm, EditRecordingFormComplete, EditRecordingFormPending, QuickCreateRecordingForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from recordings.models import Recording, RadioStation
from datetime import datetime, timedelta
import pytz
from recordings.tasks import record_show
from django.shortcuts import get_object_or_404
from celery.task.control import revoke

# Create your views here.
@login_required(login_url='/login/')
def account_view(response, username):
  if response.method == "POST":
    form = QuickCreateRecordingForm(response.POST)
    if form.is_valid():
      title = form.cleaned_data['title']
      radio_station = form.cleaned_data['radio_station']
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
        public         = True,
        start_datetime = start_datetime_aware,
        end_datetime   = end_datetime_aware
        )

      task = record_show.apply_async(args=[recording.id], eta=recording.start_datetime)
      recording.task_id = task.id
      recording.save()
      form = QuickCreateRecordingForm()
      string = "Your " + radio_station.name + " recording has been scheduled."
      messages.success(response, "Your recording has been scheduled.")
  else:
    form = QuickCreateRecordingForm()
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

@login_required(login_url='/login/')
def recordings_view(response, username):
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    return redirect(redirect_string)
  user = User.objects.get(username=username)
  recordings = user.recordings.order_by('-end_datetime')
  context = {
  "recordings" : recordings,
  }
  return render(response, 'account/my_recordings.html', context)

@login_required(login_url='/login/')
def edit_view(response, username, recording_id):
  timezone = pytz.timezone("Europe/London")
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    return redirect(redirect_string)
  recording = Recording.objects.get(pk=recording_id)
  start_within_minute = timezone.localize(datetime.now()) + timedelta(seconds=60) > recording.start_datetime.astimezone(timezone)
  if not recording.status == "pending" or start_within_minute:
    display_time = False
    form = EditRecordingFormComplete(instance=recording)
    if response.method == "POST":
      form = EditRecordingFormComplete(response.POST)
      if form.is_valid():
        recording.title = form.cleaned_data['title']
        recording.description = form.cleaned_data['description']
        recording.public = form.cleaned_data['public']
        recording.tags.set(form.cleaned_data['tags'])
        recording.save()
        messages.success(response, "Recording information has been updated.")
  else:
    display_time = True
    start_datetime_aware = recording.start_datetime.astimezone(timezone)
    end_datetime_aware   = recording.end_datetime.astimezone(timezone)
    form = EditRecordingFormPending({
      'title' : recording.title,
      'description' : recording.description,
      'radio_station' : recording.radio_station.id,
      'public'        : recording.public,
      'start_time' : start_datetime_aware.strftime("%H:%M:%S"),
      'end_time'   : end_datetime_aware.strftime("%H:%M:%S"),
      'start_date' : start_datetime_aware.date(),
      'end_date' : end_datetime_aware.date()
      })

    if response.method == "POST":
      form = EditRecordingFormPending(response.POST)
      if form.is_valid():
        title = form.cleaned_data['title']
        radio_station = form.cleaned_data['radio_station']
        public = form.cleaned_data['public']
        start_datetime = datetime.combine(form.cleaned_data['start_date'],
                                        form.cleaned_data['start_time'])
        end_datetime = datetime.combine(form.cleaned_data['end_date'],
                                      form.cleaned_data['end_time'])
        recording.tags.set(form.cleaned_data['tags'])
        timezone = pytz.timezone("Europe/London")
        start_datetime_aware = timezone.localize(start_datetime)
        end_datetime_aware = timezone.localize(end_datetime)
        recording.title = title
        recording.radio_station = radio_station
        recording.public = public
        recording.start_datetime = start_datetime_aware
        recording.end_datetime = end_datetime_aware
        revoke(recording.task_id)
        task = record_show.apply_async(args=[recording.id], eta=recording.start_datetime)
        recording.task_id = task.id
        recording.save()
        messages.success(response, "Recording information has been updated.")

  user = User.objects.get(username=username)
  recordings = user.recordings.order_by('-end_datetime')
  context = {
    "recording" : recording,
    "recordings" : recordings,
    "form" : form,
    "display_time" : display_time
  }
  return render(response, 'account/edit.html', context)

@login_required(login_url='/login/')
def create_view(response, username):
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    return redirect(redirect_string)
  user = response.user
  if response.method == "POST":
    form = CreateRecordingForm(response.POST)
    if form.is_valid():
      title = form.cleaned_data['title']
      description = form.cleaned_data['description']
      radio_station = form.cleaned_data['radio_station']
      tags = form.cleaned_data['tags']
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
        description    = description,
        radio_station  = radio_station,
        public         = public,
        start_datetime = start_datetime_aware,
        end_datetime   = end_datetime_aware
        )
      recording.tags.set(tags)
      task = record_show.apply_async(args=[recording.id], eta=recording.start_datetime)
      recording.task_id = task.id
      recording.save()
      # record_show.delay(recording.id)
      string = "Your " + radio_station.name + " recording has been scheduled."
      messages.success(response, "Your recording has been scheduled.")
      redirect_string = "/" + str(user.username) + "/myrecordings"
      return redirect(redirect_string)
  else:
    form = CreateRecordingForm()
  context = {
  "user" : user,
  "form" : form
  }
  return render(response, 'account/create.html', context)

@login_required(login_url='/login/')
def delete_view(response, username, recording_id):
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    return redirect(redirect_string)
  try:
    recording = Recording.objects.get(pk=recording_id)
    if recording.status != 'complete':
      revoke(recording.task_id)
    recording.delete()
    messages.success(response, "Your recording has been deleted.")
  except:
    pass
  finally:
    user = User.objects.get(username=username)
    redirect_string = "/" + str(user.username) + "/myrecordings"
    return redirect(redirect_string)

@login_required(login_url='/login/')
def listen_view(response, username, recording_id):
  if not check_profile_owner(response, username):
    redirect_string = "/recordings/" + str(recording_id)
    return redirect(redirect_string)
  recording = Recording.objects.get(pk=recording_id)
  user = User.objects.get(username=username)
  recordings = user.recordings.order_by('-end_datetime')
  context = {
    "recording" : recording,
    "recordings" : recordings,
    "user"      : user,
  }
  return render(response, 'account/listen.html', context)


@login_required(login_url='/login/')
def settings_view(response, username):
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    return redirect(redirect_string)
  settings = ["General", "Security and Login", "Privacy", "Language and Region", "Notifications", "Mobile"]
  context = {
    "settings" : settings
  }
  return render(response, 'account/settings.html', context)

def check_profile_owner(response, username):
  if response.user.username != username:
    return False
  return True
