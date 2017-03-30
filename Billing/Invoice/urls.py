import operator
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from Invoice.views import * 

urlpatterns = [
	url(r'^v1/generatebill/$', csrf_exempt(GenerateBill.as_view())),
	url(r'^v1/payment/$', csrf_exempt(Payment.as_view())),
	url(r'^v1/transactions/$', csrf_exempt(TransactionsAPI.as_view())),
	url(r'^v1/balances/$', csrf_exempt(BalanceAPI.as_view())),
]