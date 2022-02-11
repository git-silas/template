import os
import platform
from dotenv import load_dotenv

from configparser import ConfigParser

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


DEBUG = False
CSRF_ENABLED = True

SECRET_KEY = "".join(tuple(platform.uname()._asdict().values()) + platform.python_build())

REPOSITORY = "ram://"
LOG_LEVEL = "NOTSET"
AUTH_URL = "http://localhost:5000"

TESTING = os.environ.get("TESTING", False)

AUTH_CASE = False
DEFAULT_TZ = "Europe/Berlin"
URL_PREFIX = "/"


DB_TYPE = "postgres"
DB_HOST = "localhost"
DB_DATABASE = "template"
DB_USER = "postgres"
DB_PW = "postgres!QS783mx7g"
DB_PORT = "5432"

MAIL_SERVER = "localhost"
MAIL_PORT = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = None
MAIL_PASSWORD = None
