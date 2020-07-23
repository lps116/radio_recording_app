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

AWS_ACCESS_KEY_ID = 'AKIA5LS7FIRFIXSJIJ7I'
AWS_SECRET_ACCESS_KEY = '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'

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
    print("recording started")
    recording.status = "in progress"
    recording.save()
    print(url)
    end_time         = recording.end_datetime
    chunk_size       = 256
    file_name        = recording.user.username + "-rec" + str(recording.id) + ".mp3"
    file_path        = settings.BASE_DIR + "/" + file_name
    session          = requests.Session()
    request          = session.get(url, stream=True)
    print('trying to open file')
    print(file_path)
    print(open(file_path, "wb"))
    with open(file_path, "wb") as file:
      print('managed to open file')
      for chunk in request.iter_content(chunk_size = chunk_size):
        print('writing content')
        file.write(chunk)
        if timezone.now() > end_time:
          session = boto3.Session(
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                  )
          s3 = session.resource('s3')
          bucket_name = "test-bucket-for-radio"
          s3.meta.client.upload_file(Filename=file_path,
                                    Bucket=bucket_name,
                                    Key=file_name)

          # print('saving file to s3')
          # s3_client = boto3.client('s3')
          # try:
          #   response = s3_client.upload_file(file_path, bucket, 'test.mp3')
          # except ClientError as e:
          #   logging.error(e)

          file.close()
          recording.file = recording.user.username + "-rec" + str(recording.id) + ".mp3"
          recording.status = "complete"
          recording.save()
          request.connection.close()
          print('saved')
          print(recording.file)
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
    print('checking if url valid...')
    print(request.status_code)
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
