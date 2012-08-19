# Import Django
from django.conf.urls.defaults import patterns, include, url

# Import views
from .views.builder import *
from .views.page import *

urlpatterns = patterns('builder.views.builder',
	url(r'^(?P<id>\d+)$', BuilderView.as_view(), name='builder_page'),
)

urlpatterns += patterns('builder.views.pages',
	url(r'^page/all/$', PageView.as_view(), name='page_all'),
	url(r'^page/create/$', PageView.as_view(), name='page_create', kwargs={'action' : 'create'}),
	url(r'^page/delete/(?P<id>\d+)/$', PageView.as_view(), name='page_delete', kwargs={'action' : 'delete'}),
)