from celery import shared_task
from .models import Recording, RadioStation
from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.utils import timezone
import json
import boto3
from botocore.exceptions import ClientError
import logging
import os

@shared_task
def record_show(id):
  recording        = Recording.objects.get(id=id)
  radio_station    = recording.radio_station
  url              = radio_station.streaming_link
  if not streaming_link_is_valid(url):
    new_link = find_new_link(radio_station.id)
    if new_link is not None:
      url = new_link
      radio_station.streaming_link = url
      radio_station.save()
    else:
      recording.status = "complete"
      recording.save()
      return
  try:
    recording.status = "in progress"
    recording.save()
    end_time         = recording.end_datetime
    chunk_size       = 256
    file_name        = recording.user.username + "-rec" + str(recording.id) + ".mp3"
    file_path        = settings.BASE_DIR + "/" + file_name
    session          = requests.Session()
    request          = session.get(url, stream=True)
    with open(file_path, "wb") as file:
      for chunk in request.iter_content(chunk_size = chunk_size):
        file.write(chunk)
        if timezone.now() > end_time:
          session = boto3.Session(
                  aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                  aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                  )
          s3 = session.resource('s3')
          s3.meta.client.upload_file(Filename=file_path,
                                    Bucket=os.environ.get('AWS_BUCKET_NAME'),
                                    Key=file_name)

          recording_url = "https://%s.s3.eu-west-2.amazonaws.com/%s" % (os.environ.get('AWS_BUCKET_NAME'), file_name)

          file.close()
          recording.file = recording_url
          recording.status = "complete"
          recording.save()
          request.connection.close()
          return
  except:
    print('recoridng failed')
    recording.status = "complete"
    recording.save()
    return

def streaming_link_is_valid(url):
  if not len(url):
    return False
  try:
    session = requests.Session()
    request = session.get(url, stream=True)
    if request.status_code == 200 and request.headers.get('content-type') == 'audio/mpeg':
      request.connection.close()
      return True
  except:
    return False

def find_new_link(id):
  radio_station = RadioStation.objects.get(id=id)
  radio_station_name = modify_bbc_names_reverse(radio_station.name)
  streaming_links_json = get_radio_links(station=radio_station_name)
  if len(streaming_links_json):
    for link in streaming_links_json['results']:
      if streaming_link_is_valid(link['u']):
        return link['u']
  return None

def get_radio_links(station, country="UK", genre="ALL" ):
  url = "https://30-000-radio-stations-and-music-charts.p.rapidapi.com/rapidapi"
  querystring = {"country":country,"keyword":station,"genre":genre}
  headers = {
      'x-rapidapi-host': "30-000-radio-stations-and-music-charts.p.rapidapi.com",
      'x-rapidapi-key' : os.environ.get("RAPID_API_KEY_ONE")
      }
  response = requests.request("GET", url, headers=headers, params=querystring)
  return json.loads(response.text)


def modify_bbc_names_reverse(name):
  if name == "BBC Radio 1":
    return "BBC 1"
  elif name == "BBC Radio 2":
    return "BBC 2"
  elif name == "BBC Radio 3":
    return "BBC 3"
  elif name == "BBC Radio 4":
    return "BBC 4"
  elif name == "BBC World Service":
    return "BBC World"
  else:
    return name
