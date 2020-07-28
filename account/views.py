from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CreateRecordingForm, EditRecordingFormComplete, EditRecordingFormPending
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from recordings.models import Recording, RadioStation
from datetime import datetime
import pytz
from recordings.tasks import record_show
from django.shortcuts import get_object_or_404
from celery.task.control import revoke



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

      task = record_show.apply_async(args=[recording.id], eta=recording.start_datetime)
      recording.task_id = task.id
      recording.save()
      # record_show.delay(recording.id)
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
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    print('wrong user')
    return redirect(redirect_string)
  recording = Recording.objects.get(pk=recording_id)
  if not recording.status == "pending":
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
    if response.method == "POST":
      print('creating edit form')
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
        print('recording edited...')
        messages.success(response, "Recording information has been updated.")

  recording = Recording.objects.get(pk=recording_id)
  if not recording.status == "pending":
    form = EditRecordingFormComplete(instance=recording)
  else:
    form = EditRecordingFormPending(instance=recording)

  context = {
    "recording" : recording,
    "form" : form
  }
  return render(response, 'account/edit.html', context)

@login_required(login_url='/login/')
def create_view(response, username):
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    print('create not the right user')
    return redirect(redirect_string)
  user = response.user
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

      task = record_show.apply_async(args=[recording.id], eta=recording.start_datetime)
      recording.task_id = task.id
      recording.save()
      # record_show.delay(recording.id)
      string = "Your " + radio_station.name + " recording has been scheduled."
      messages.success(response, "Your recording has been scheduled.")
      redirect_string = "/" + str(user.username) + "/myrecordings"
      return redirect(redirect_string)
  form = CreateRecordingForm()
  context = {
  "user" : user,
  "form" : form
  }
  return render(response, 'account/create.html', context)

@login_required(login_url='/login/')
def delete_view(response, username, recording_id):
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

def listen_view(response, username, recording_id):
  recording = Recording.objects.get(pk=recording_id)
  user = response.user
  context = {
  "recording" : recording,
  "user"      : user,
  }
  return render(response, 'account/listen.html', context)


@login_required(login_url='/login/')
def settings_view(response, username):
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    return redirect(redirect_string)
  context = {}
  return render(response, 'account/settings.html', context)

def check_profile_owner(response, username):
  if response.user.username != username:
    return False
  return True
