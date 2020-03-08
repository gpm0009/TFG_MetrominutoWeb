import os


class Config(object):
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

