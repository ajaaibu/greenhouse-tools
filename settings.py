import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SYSTEM_ID = os.environ.get('SYSTEM_ID')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
SYNC_URL = os.environ.get('SYNC_URL')
SYNC_LIMIT = int(os.environ.get('SYNC_LIMIT',10))
CLOUD_USERNAME = os.environ.get('CLOUD_USERNAME')
CLOUD_PASSWORD = os.environ.get('CLOUD_PASSWORD')