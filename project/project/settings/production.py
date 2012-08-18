from project.settings.defaults import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

INSTALLED_APPS = (
	'gunicorn',
)