# Import Django
from django.conf.urls.defaults import patterns, include, url

# Import views
from .views.page import *

urlpatterns = patterns('builder.views.pages',
	url(r'^page/create/$', PageCreate.as_view(), name='page_create'),
)