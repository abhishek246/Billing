from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, QueryDict
from django.db import DatabaseError
from django.db import connection
from django.db import transaction
from django.db import models
from django.db.models import Count, F, Sum

from datetime import datetime
from Areas.models import *
from Vendors.models import Vendor
from Indent.models import Publisher,Indent
from Billing.base import decorator_4xx

import json

class IndentAPI(View):
    ''''''
    def __init__(self):
        ''''''
        self.model = Indent
        self.status_code = 200
        self.response_message = 'OK' 
        self.response = {
            'res_data': {}
        }

    @decorator_4xx([])
    def dispatch(self, *args, **kwargs):
        query_set = super(self.__class__, self).dispatch(*args, **kwargs)
        if self.status_code == 200:
            seialized = self.model.objects.serializer(query_set)
            self.response['res_data'] = seialized
        return JsonResponse(self.response, status=200)

    def get(self, request, *args, **kwargs):
        params = request.GET
        _month = params.get('month')
        _year = params.get('year')
        _publisher_id = params.get('publisher')

        try:
            _vendor = Vendor.objects.get(pk=params.get('vendor_id'))
            _publisher = Publisher.objects.get(pk=_publisher_id)
            if params.get('vendor_id'):
                _indent_details= Indent.objects.filter(vendor=_vendor, date__year=_year,\
                                                       date__month=_month, publisher=_publisher)
            else:
                raise AssertionError('Mandatory Params Missing') 
        except (Vendor.DoesNotExist, Publisher.DoesNotExist) as ex:
            self.status = 400
        except AssertionError as ex:
            self.status = 400 
        return _indent_details


class BulkAddIndent(View):
    def __init__(self):
        ''''''
        self.model = Area
        self.status_code = 200
        self.response_message = 'OK' 
        self.response = {
            'res_data': {}
        }

    @decorator_4xx([])
    def dispatch(self, *args, **kwargs):
        query_set = super(self.__class__, self).dispatch(*args, **kwargs)
        if self.status_code == 200:
            #seialized = self.model.objects.serializer(query_set)
            self.response['res_data'] = {} #seialized
        return JsonResponse(self.response, status=201)


    def post(self, request, *args, **kwargs):
        #import pdb; pdb.set_trace()
        params = json.loads(request.body)
        _indents = json.loads(params.get('indent'))
        _date = params.get('date')

        _date = datetime.strptime(_date, "%d-%m-%Y")

        indent_objects = list()
        try:
            _publisher = Publisher.objects.get(pk=params.get('publisher_id'))
            for indent in _indents:
                try:
                    _vendor = Vendor.objects.get(pk=indent.get('id'))
                    
                    Indent.objects.get(vendor=_vendor, publisher=_publisher, date=_date)
                    raise AssertionError("Few Vendor Already have a indent create for the date")
                except Indent.DoesNotExist as ex:
                    _indent = Indent(vendor=_vendor, publisher=_publisher,
                                     indent=indent.get('indent'), date=_date)
                    indent_objects.append(_indent)
                except (Vendor.DoesNotExist,) as ex:
                    raise AssertionError('Vendor or Publisher Id provieded Does not Exists')
            with transaction.atomic():
               Indent.objects.bulk_create(indent_objects)
        except (Publisher.DoesNotExist,) as ex:
            self.status_code = 400
        except AssertionError as ex:
            self.status_code = 400
        return list()


class PublisherAPI(View):
    def __init__(self):
        self.model = Publisher
        self.status_code = 200
        self.response_message = 'OK' 
        self.response = {
            'res_data': {}
        }
    
    @decorator_4xx([])
    def dispatch(self, *args, **kwargs):
        query_set = super(self.__class__, self).dispatch(*args, **kwargs)
        if self.status_code == 200:
            seialized = self.model.objects.serializer(query_set)
            self.response['res_data'] = seialized
        return JsonResponse(self.response, status=201)

    def get(self, request, *args, **kwargs):
        return Publisher.objects.all()


