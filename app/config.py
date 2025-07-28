import os
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'MW1ER2S3!@#$'
