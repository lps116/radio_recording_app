from celery import shared_task
from .models import Recording, RadioStation
from datetime import datetime, timedelta
import requests
from django.conf import settings
from django.utils import timezone
import json

@shared_task
def record_show(id):
  recording        = Recording.objects.get(id=id)
  radio_station    = recording.radio_station
  url              = radio_station.streaming_link
  if not streaming_link_is_valid(url):
    new_link = find_new_link(radio_station.id)
    if  new_link is not None:
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
    print(url)
    end_time         = recording.end_datetime
    chunk_size       = 256
    file_path        = settings.MEDIA_ROOT + 'media/' + recording.user.username + "-rec" + str(recording.id) + ".mp3"
    session          = requests.Session()
    request          = session.get(url, stream=True)
    with open(file_path, "wb") as file:
      for chunk in request.iter_content(chunk_size = chunk_size):
        file.write(chunk)
        if timezone.now() > end_time:
          file.close()
          recording.file = 'media/' + recording.user.username + "-rec" + str(recording.id) + ".mp3"
          recording.status = "complete"
          recording.save()
          request.connection.close()
          return
  except:
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
      # 'x-rapidapi-key': "81f9bb4c51msh270013cb0fdf3fdp1f75dejsnfa321cc6bd26"
      'x-rapidapi-key': "deffea4b89msha39476b3fcfbd63p14289djsn599001cd7c59"
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