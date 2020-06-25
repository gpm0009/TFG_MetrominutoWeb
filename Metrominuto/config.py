"""
    config

    This file contains classes to be uses as the configuration
    for the application.
    Development, production and test in case it is needed.
"""
import os


class Config(object):
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


class ProductionConfig(Config):
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
