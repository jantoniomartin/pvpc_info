from django.conf.urls import patterns, include, url

from prices.views import *

urlpatterns = patterns('prices.views',
	url(r'^$', HomeView.as_view(), name='prices_home'),
)
