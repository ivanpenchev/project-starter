from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from project.views import (LoginView, HomeView, LogoutView,
                           SignupView, DashboardView, LostPasswordView, SetPasswordView)

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^sign-in$', LoginView.as_view(), name='sign-in'),
    url(r'^sign-in/confirm/(?P<type>.+)$', LoginView.as_view(), name='sign-in-confirm', kwargs={'confirm':True}),
    url(r'^sign-in/(?P<type>.+)$', LoginView.as_view(), name='sign-in-special'),
    url(r'^sign-up$', SignupView.as_view(), name='sign-up'),
    url(r'^account/password$', SetPasswordView.as_view(), name='set-password'),
    url(r'^password/lost$', LostPasswordView.as_view(), name='lost-password'),
    url(r'^dashboard', DashboardView.as_view(), name='dashboard'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    url(r'^builder/', include('builder.urls')),
)

if not settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
