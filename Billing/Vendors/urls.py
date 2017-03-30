import operator
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Vendors.views import *

urlpatterns = [
	url(r'^v1/vendor/$', csrf_exempt(VendorAPI.as_view())),
]