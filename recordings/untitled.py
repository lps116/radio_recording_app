# import boto
# import boto.s3
# import sys
# from boto.s3.key import Key

# AWS_ACCESS_KEY_ID = 'AKIA5LS7FIRFIXSJIJ7I'
# AWS_SECRET_ACCESS_KEY = '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'

# s3_connection = boto.connect_s3()
# bucket = s3_connection.get_bucket('radio-recording-app')
# key = boto.s3.key.Key(bucket, 'favicon.png')
# with open('favicon.png') as f:
#     key.send_file(f)


# import boto3

# session = boto3.Session(
#     aws_access_key_id=AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
# )
# s3 = session.resource('s3')
# Filename - File to upload
# Bucket - Bucket to upload to (the top level directory under AWS S3)
# Key - S3 object name (can contain subdirectories). If not specified then file_name is used
# s3.meta.client.upload_file(Filename='/Users/linus.strobel/code/lps30/s3_test/favicon.png', Bucket='test-bucket-for-radio', Key='favicon.png')


# import logging
import boto3
# from botocore.exceptions import ClientError
s3 = boto3.resource('s3')
print(s3)
print('hello')


  """Upload a file to an S3 bucket
  :param file_name: File to upload
  :param bucket: Bucket to upload to
  :param object_name: S3 object name. If not specified then file_name is used
  :return: True if file was uploaded, else False
  """
  # If S3 object_name was not specified, use file_name

# if object_name is None:
#   object_name = file_name
  # Upload the file
# s3_client = boto3.client('s3')
# try:
#   response = s3_client.upload_file('favicon.png', 'test-bucket-for-radio', 'favicon.png')
#   print(response)
#   print('hello')
# except ClientError as e:
#   logging.error(e)
#   print('error')
#   return False
# return True
