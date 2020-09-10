from django.core.management.base import BaseCommand, CommandError
from recordings.models import Recording, RadioStation, Tag
from django.contrib.auth.models import User
from faker import Faker
import factory
import requests
import json
from datetime import datetime, timedelta
from random import randint, choice
from django.utils import timezone
import os

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    # methods run when seeding proccess starts
    # first clear the database and then populate with new data
    def handle(self, *args, **options):
        print("clearing database...")
        clear_database(self, options['mode'])
        print('done...')
        print('seeding data...')
        run_seed(self, options['mode'])
        print('done.')

# adds all the data to database
def run_seed(self, mode):
  print("adding users...")
  create_users()
  print("adding radio stations...")
  create_radio_stations()
  print("adding tags...")
  create_tags()
  print("adding recordings...")
  create_recordings()


# clears all the data in the databse
def clear_database(self, mode):
  user = User.objects.all().first()
  User.objects.all().delete()
  user.save()
  Recording.objects.all().delete()
  RadioStation.objects.all().delete()
  Tag.objects.all().delete()


# creates recordings with fake names, descriptions
# random users, radio station, tags
def create_recordings():
  faker = Faker()
  for i in range(0, 10):
    start_time_skew = randint(1, 30)
    end_time_skew = randint(31, 60)
    day_skew = randint(1, 30)
    recording = Recording(
      user           = User.objects.order_by("?").first(),
      radio_station  = RadioStation.objects.order_by("?").first(),
      title          = faker.text()[:20],
      description    = faker.text(),
      start_datetime = timezone.now() + timedelta(days=day_skew, minutes=start_time_skew),
      end_datetime   = timezone.now() + timedelta(days=day_skew, minutes=end_time_skew),
      status         = choice(["pending", "complete"]),
      public         = choice([False, True, True, True])
      )
    recording.save()
    random_tags = Tag.objects.order_by("?")
    recording.tags.add(random_tags[0], random_tags[1])

# creates users with Fake information
def create_users():
  faker = Faker()
  for i in range(0, 6):
    first_name = faker.first_name()
    username   = first_name + "123"
    user = User.objects.create_user(
      first_name = first_name,
      last_name  = faker.last_name(),
      email      = faker.email(),
      username   = username,
      password   = "password123",
      )
    user.save()

# populates the database with some tags
def create_tags():
  # api for course subjects - subjects used as tags
  response = requests.request("GET", "https://www.reed.co.uk/courses/api/v4/subjects")
  if response.status_code == 200:
    data = json.loads(response.text)
    for topic in data:
      tag = topic['name']
      new_tag = Tag(
         tag = tag
        )
      new_tag.save()
    response.connection.close()


# adds radio stations to DB
def create_radio_stations():
  # get links with BBC in name (default of method)
  stations = get_radio_stations_with_links()
  for station in stations['results']:
    # change BBC station names
    station_name = modify_bbc_names(station['n'])
    # if streaming link is valid save the station name and link to DB
    if streaming_link_is_valid(station['u']):
      streaming_link = station['u']
      new_radio_station = RadioStation(
        name=station_name,
        streaming_link=streaming_link
        )
      new_radio_station.save()
    else:
      continue

# requests radio station information from API
# returns data in JSON format.
def get_radio_stations_with_links(country="UK", station="bbc", genre='ALL'):
  url = "https://30-000-radio-stations-and-music-charts.p.rapidapi.com/rapidapi"
  querystring = {"country":country,"keyword":station,"genre":genre}
  headers = {
      'x-rapidapi-host': "30-000-radio-stations-and-music-charts.p.rapidapi.com",
      'x-rapidapi-key': os.environ.get("RAPID_API_KEY_TWO")
  }
  response = requests.request("GET", url, headers=headers, params=querystring)
  return json.loads(response.text)

# converts BBC radio names to official name
# to be displayed on website and stored in DB
def modify_bbc_names(name):
  if name == "BBC 1":
    return "BBC Radio 1"
  elif name == "BBC 2":
    return "BBC Radio 2"
  elif name == "BBC 3":
    return "BBC Radio 3"
  elif name == "BBC 4":
    return "BBC Radio 4"
  elif name == "BBC World":
    return "BBC World Service"
  else:
    return name

# check streaming link is valid by checking if status is 200
# and content type is audio/mpeg
def streaming_link_is_valid(link):
  if not len(link):
    return False
  try:
    session = requests.Session()
    request = session.get(link, stream=True)
    if request.status_code == 200 and request.headers.get('content-type') == 'audio/mpeg':
      request.connection.close()
      return True
  except:
    try:
      request.connection.close()
    except:
      pass
    return False
