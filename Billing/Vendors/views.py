from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, QueryDict
from django.db import DatabaseError
from django.db import connection
from django.db import transaction
from django.db import models
from django.db.models import Count, F, Sum

from datetime import datetime
from Vendors.models import *

class VendorAPI(View):
    ''''''
    def __init__(self):
        ''''''
        self.model = Vendor
        self.status_code = 200
        self.response_message = 'OK' 
        self.response = {
            'res_data': {}
        }

    def dispatch(self, *args, **kwargs):
        query_set = super(self.__class__, self).dispatch(*args, **kwargs)
        if self.status_code == 200:
           seialized = self.model.objects.serializer(query_set)
           self.response['res_data'] = seialized
        return JsonResponse(self.response, status=self.status_code)

    def get(self, request, *args, **kwargs):
        params = request.GET
        _vendor_id = params.get('vendor_id', None)
        _area_id = params.get('area_id')
        if _vendor_id:
            try:
                _vendor = Vendor.objects.get(pk=_vendor_id)
            except (Vendor.DoesNotExists, ) as ex:
                self.status_code = 400
        else:
            _vendor = Vendor.objects.filter(area_id=_area_id)
        return _vendor

    def post(self, request, *args, **kwargs):
        params = request.POST
        _vendor = Vendor(name=params.get('name'), mobile_number=params.get('mobile_number'),\
                         abbrivation=params.get('abbv'), area_id=params.get('area_id'))
        with transaction.atomic():
            from Invoice.models import Balance
            _vendor.save()
            _balance = Balance(vendor=_vendor, runningvalue=0)
            _balance.save()
        return _vendor