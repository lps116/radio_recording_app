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

# view for account overview page
# loads user's recordings sorted by status and quick schedule recording form
@login_required(login_url='/login/')
def account_view(response, username):
  # if form submitted by user
  if response.method == "POST":
    form = QuickCreateRecordingForm(response.POST)
    # check if form is valid (based on clean method in form class)
    if form.is_valid():
      # clean form data
      title, radio_station = get_title_and_radio_station(form)
      start_datetime_aware, end_datetime_aware = get_localized_datetimes(form)
      # create recording object
      recording = Recording.objects.create(
        user           = response.user,
        title          = title,
        radio_station  = radio_station,
        public         = True,
        start_datetime = start_datetime_aware,
        end_datetime   = end_datetime_aware
        )
      # schedule and save to DB
      recording.task_id = schedule_recording(recording)
      recording.save()
      form = QuickCreateRecordingForm()
      messages.success(response, "Your recording has been scheduled.")
  else:
    form = QuickCreateRecordingForm()
  user = User.objects.get(username=username)
  scheduled_recordings, completed_recordings, inprogress_recordings = get_sorted_user_recordings(user)
  context = {
        "user" : user,
        "scheduled_recordings"  : scheduled_recordings,
        "completed_recordings"  : completed_recordings,
        "inprogress_recordings" : inprogress_recordings,
        }
  if user == response.user:
    # render form if the user is the profile owner
    context["form"] = form
    return render(response, 'account/profile.html', context)
  else:
    return render(response, 'account/profile.html', context)

# my recordings page
# simply load all of user recordings and order by endtime
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

# view for editing recording pages
# loads different forms based on the status of the recording to be edited
@login_required(login_url='/login/')
def edit_view(response, username, recording_id):
  timezone = pytz.timezone("Europe/London")
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    return redirect(redirect_string)

  recording = Recording.objects.get(pk=recording_id)
  start_within_minute = timezone.localize(datetime.now()) + timedelta(seconds=60) > recording.start_datetime.astimezone(timezone)
  # logic for completed recording
  if not recording.status == "pending" or start_within_minute:
    form = EditRecordingFormComplete(instance=recording)
    # if form submitted
    if response.method == "POST":
      form = EditRecordingFormComplete(response.POST)
      if form.is_valid():
        # set the new values
        recording = set_recording_title_des_pub_tags(recording, form)
        recording.save()
        messages.success(response, "Recording information has been updated.")
  # if recording status pending (user can still change the time)
  else:
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
      'end_date' : end_datetime_aware.date(),
      'tags'     : recording.tags.all()
      })
    # if user sumbits form
    if response.method == "POST":
      form = EditRecordingFormPending(response.POST)
      if form.is_valid():
        # clean data and set recording values
        _, radio_station = get_title_and_radio_station(form)
        start_datetime_aware, end_datetime_aware = get_localized_datetimes(form)
        recording = set_recording_title_des_pub_tags(recording, form)
        recording.radio_station = radio_station
        recording.start_datetime, recording.end_datetime = start_datetime_aware, end_datetime_aware
        # delte previous taks from queue
        revoke(recording.task_id)
        # schedule new task and save update to DB
        recording.task_id = schedule_recording(recording)
        recording.save()
        messages.success(response, "Recording information has been updated.")
  user = User.objects.get(username=username)
  recordings = user.recordings.order_by('-end_datetime')
  context = {
    "recording" : recording,
    "recordings" : recordings,
    "form" : form,
  }
  return render(response, 'account/edit.html', context)

# view for complete recording form page
@login_required(login_url='/login/')
def create_view(response, username):
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    return redirect(redirect_string)
  # if form submitted
  if response.method == "POST":
    form = CreateRecordingForm(response.POST)
    # check if form valid
    if form.is_valid():
      # clean form data
      title, radio_station = get_title_and_radio_station(form)
      description = form.cleaned_data['description']
      tags = form.cleaned_data['tags']
      public = form.cleaned_data['public']
      start_datetime_aware, end_datetime_aware = get_localized_datetimes(form)
      # create recording object
      recording = Recording.objects.create(
        user           = response.user,
        title          = title,
        description    = description,
        radio_station  = radio_station,
        public         = public,
        start_datetime = start_datetime_aware,
        end_datetime   = end_datetime_aware
        )
      recording.tags.set(tags)
      # schedule and save to DB
      recording.task_id = schedule_recording(recording)
      recording.save()
      messages.success(response, "Your recording has been scheduled.")
      redirect_string = "/" + str(username) + "/myrecordings"
      return redirect(redirect_string)
  else:
    # load empty for if get request
    form = CreateRecordingForm()
  context = {
  "user" : response.user,
  "form" : form
  }
  return render(response, 'account/create.html', context)

# view deletes recordings
# view ends in redirect not in template render
@login_required(login_url='/login/')
def delete_view(response, username, recording_id):
  if not check_profile_owner(response, username):
    redirect_string = "/" + username
    return redirect(redirect_string)
  try:
    recording = Recording.objects.get(pk=recording_id)
    # remove task from queue if not completed
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

# view for user's recording
# template loads specifc recroding and all a user's recordings
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


# view for settings page - settings list only for display
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

# checks if the current user is the profile owner
def check_profile_owner(response, username):
  if response.user.username != username:
    return False
  return True

# converts form date/time input into format accepted by recording model
def get_localized_datetimes(form):
  start_datetime = datetime.combine(form.cleaned_data['start_date'],
                                        form.cleaned_data['start_time'])
  end_datetime = datetime.combine(form.cleaned_data['end_date'],
                                      form.cleaned_data['end_time'])
  timezone = pytz.timezone("Europe/London")
  start_datetime_aware = timezone.localize(start_datetime)
  end_datetime_aware = timezone.localize(end_datetime)
  return start_datetime_aware, end_datetime_aware

# returns cleaned title and radio_station from form
def get_title_and_radio_station(form):
  title = form.cleaned_data['title']
  radio_station = form.cleaned_data['radio_station']
  return title, radio_station

# adds recordings task to task queue and returns ID
def schedule_recording(recording):
  task = record_show.apply_async(args=[recording.id], eta=recording.start_datetime)
  return task.id

# returns user recordings sorted by status
def get_sorted_user_recordings(user):
  scheduled_recordings = user.recordings.filter(status="pending").order_by('start_datetime')
  completed_recordings = user.recordings.filter(status="complete").order_by('-end_datetime')
  inprogress_recordings = user.recordings.filter(status="in progress").order_by('start_datetime')
  return scheduled_recordings, completed_recordings, inprogress_recordings

# set title, description, public and tag form input values
def set_recording_title_des_pub_tags(recording, form):
  recording.title = form.cleaned_data['title']
  recording.description = form.cleaned_data['description']
  recording.public = form.cleaned_data['public']
  recording.tags.set(form.cleaned_data['tags'])
  return recording
