# Import Django
from django.conf.urls.defaults import patterns, include, url

# Import views
from .views.builder import *
from .views.page import *
from .views.ajax import *

urlpatterns = patterns('builder.views.builder',
	url(r'^(?P<id>\d+)/$', BuilderView.as_view(), name='builder-page'),
	
	url(r'^(?P<id>\d+)/landing-page/$', BuilderView.as_view(), name='landing-page', kwargs={'action' : 'landing'}),
	url(r'^(?P<id>\d+)/sharing-page/$', BuilderView.as_view(), name='sharing-page', kwargs={'action' : 'sharing'}),
	url(r'^(?P<id>\d+)/confirmation-email/$', BuilderView.as_view(), name='confirm-email', kwargs={'action' : 'email'}),
	url(r'^(?P<id>\d+)/site-settings/$', BuilderView.as_view(), name='site-settings', kwargs={'action' : 'settings'}),
	url(r'^(?P<id>\d+)/review-page/$', BuilderView.as_view(), name='review-page', kwargs={'action' : 'review'}),
	
	# Different URLs for JSON loading - prevents from loading raw JSON on the page
	url(r'^(?P<id>\d+)/landing-page/(?P<json>.+)/$', BuilderView.as_view(), name='landing-page', kwargs={'action' : 'landing'}),
	url(r'^(?P<id>\d+)/sharing-page/(?P<json>.+)/$', BuilderView.as_view(), name='sharing-page', kwargs={'action' : 'sharing'}),
	url(r'^(?P<id>\d+)/confirmation-email/(?P<json>.+)/$', BuilderView.as_view(), name='confirm-email', kwargs={'action' : 'email'}),
	url(r'^(?P<id>\d+)/site-settings/(?P<json>.+)/$', BuilderView.as_view(), name='site-settings', kwargs={'action' : 'settings'}),
	url(r'^(?P<id>\d+)/review-page/(?P<json>.+)/$', BuilderView.as_view(), name='review-page', kwargs={'action' : 'review'}),
)

urlpatterns += patterns('builder.views.pages',
	url(r'^page/all/$', PageView.as_view(), name='page-all'),
	url(r'^page/create/$', PageView.as_view(), name='page-create', kwargs={'action' : 'create'}),
	url(r'^page/delete/(?P<id>\d+)/$', PageView.as_view(), name='page-delete', kwargs={'action' : 'delete'}),
)

urlpatterns += patterns('builder.views.ajax',
	url(r'ajax/save_element/$', AjaxView.as_view(), name='save-element', kwargs={'action' : 'save_element'}),
)