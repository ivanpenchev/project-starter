from django.conf.urls import patterns, include, url
from project import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from project.views import LoginView, HomeView, LogoutView, SignupView

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^sign-in$', LoginView.as_view(), name='sign-in'),
    url(r'^sign-up$', SignupView.as_view(), name='sign-up'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),

    url(r'^builder/', include('builder.urls')),
)
