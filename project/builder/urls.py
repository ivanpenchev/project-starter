# Import Django
from django.conf.urls.defaults import patterns, include, url

# Import views
from .views.builder import *
from .views.page import *

urlpatterns = patterns('builder.views.builder',
	url(r'^(?P<id>\d+)$', BuilderView.as_view(), name='builder_page'),
)

urlpatterns += patterns('builder.views.pages',
	url(r'^page/create/$', PageCreateView.as_view(), name='page_create'),
)