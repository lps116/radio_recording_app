from django import forms
from recordings.models import Recording
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

class DateInput(forms.DateInput):
  input_type = "date"

class TimeInput(forms.TimeInput):
  input_type = 'time'

class CreateRecordingForm(forms.ModelForm):

  start_date = forms.DateField(widget=DateInput())
  start_time = forms.TimeField(widget=TimeInput())
  end_date   = forms.DateField(widget=DateInput())
  end_time   = forms.TimeField(widget=TimeInput())

  class Meta:
    model = Recording
    fields = ['title',
              'radio_station',
              'public'
              ]

  def clean(self):
    cleaned_data = super().clean()
    start_date = cleaned_data.get("start_date")
    start_time = cleaned_data.get("start_time")
    end_date   = cleaned_data.get("end_date")
    end_time   = cleaned_data.get("end_time")

    if start_date and start_time and end_date and end_time:
      start_datetime = datetime.combine(start_date, start_time)
      end_datetime   = datetime.combine(end_date, end_time)

      if start_datetime > end_datetime:
        raise ValidationError("Set an earlier start date.")

      # if start_datetime < datetime.now():
      #   raise ValidationError("Set a later start date.")

      # if datetime.now() + timedelta(seconds=30) > start_datetime:
      #   raise ValidationError("Earliest start time in 1 minute.")

      if int((end_datetime - start_datetime).total_seconds()) / 60 > 120:
        raise ValidationError("Max recording length 2 hours.")

class EditRecordingFormComplete(forms.ModelForm):

  class Meta:
    model = Recording
    fields = ['title', 'description', 'tags', 'public']
    widgets = {
      'description' : forms.Textarea(attrs={'rows':2, 'cols':15})
    }

class EditRecordingFormPending(forms.ModelForm):

  start_date = forms.DateField(widget=DateInput())
  start_time = forms.TimeField(widget=TimeInput())
  end_date   = forms.DateField(widget=DateInput())
  end_time   = forms.TimeField(widget=TimeInput())

  class Meta:
    model = Recording
    fields = ['title',
              'description',
              'radio_station',
              'tags',
              'public'
              ]

  def clean(self):
    cleaned_data = super().clean()
    start_date = cleaned_data.get("start_date")
    start_time = cleaned_data.get("start_time")
    end_date   = cleaned_data.get("end_date")
    end_time   = cleaned_data.get("end_time")

    if start_date and start_time and end_date and end_time:
      start_datetime = datetime.combine(start_date, start_time)
      end_datetime   = datetime.combine(end_date, end_time)

      if start_datetime > end_datetime:
        raise ValidationError("Set an earlier start date.")

      # if datetime.now() + timedelta(seconds=30) > start_datetime:
      #   raise ValidationError("Earliest start time in 1 minute.")

      if int((end_datetime - start_datetime).total_seconds()) / 60 > 120:
        raise ValidationError("Max recording length 2 hours.")

