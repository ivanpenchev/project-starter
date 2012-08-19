from project.settings.defaults import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

import dj_database_url
DATABASES = {
	'default': dj_database_url.config(default=os.environ.get('HEROKU_POSTGRESQL_GOLD_URL'))
}

INSTALLED_APPS = (
	'gunicorn',
)

COMPRESS_ENABLED = True