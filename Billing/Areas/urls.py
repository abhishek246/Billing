import operator
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Areas.views import *

urlpatterns = [
	#url(r'^v1/areas/(?P<area>[0-9]+)/$', csrf_exempt(AreaAPI.as_view())),
	url(r'^v1/areas/$', csrf_exempt(AreaAPI.as_view())),
]