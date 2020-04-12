"""
    config

    This file contains classes to be uses as the configuration
    for the application.
"""
import os


class Config(object):
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
