import operator
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from Indent.views import *

urlpatterns = [
	url(r'^v1/vendor/$', csrf_exempt(IndentAPI.as_view())),	
	url(r'^v1/add/$', csrf_exempt(BulkAddIndent.as_view())),
	url(r'^v1/publishers/$', csrf_exempt(PublisherAPI.as_view())),
]