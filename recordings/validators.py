from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, MinLengthValidator
import os

def validate_streaming_url(value):
  url_validator = URLValidator()
  try:
    url_validator(value)
  except:
    raise ValidationError("Invalid  URL")
  return value

def validate_title_over_ten_characters(value):
  min_length_validator = MinLengthValidator(10)
  try:
    min_length_validator(value)
  except:
    raise ValidationError("Title must be atleast 10 characters long")

def validate_description_over_thirty_characters(value):
  min_length_validator = MinLengthValidator(30)
  try:
    min_length_validator(value)
  except:
    raise ValidationError("Title must be atleast 30 characters long")

def validate_over_one_character(value):
  min_length_validator = MinLengthValidator(1)
  try:
    min_length_validator(value)
  except:
    raise ValidationError("Title must be atleast 30 characters long")

def is_mp3_file(file):
  _, extension = os.path.splitext(file.name)
  if not extension.lower() in ['.mp3']:
    raise ValidationError('File type must be MP3')





