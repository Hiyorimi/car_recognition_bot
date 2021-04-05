# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv, find_dotenv

ENV = os.environ.get('ENV') or 'development'

if ENV == 'development':
    load_dotenv(find_dotenv('./.env'))

API_TOKEN = os.environ.get('API_TOKEN') or ''
GEOCODING_API_KEY = os.environ.get('GEOCODING_API_KEY') or ''