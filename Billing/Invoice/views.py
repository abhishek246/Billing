from django.views.generic import View
from django.utils.decorators import method_decorator
from django.http import HttpResponse, JsonResponse, QueryDict
from django.db import DatabaseError
from django.db import connection
from django.db import transaction
from django.db import models
from django.db.models import Count, F, Sum

from Invoice.models import *
from Billing.base import decorator_4xx
import json

class GenerateBill(View):
    ''''''
    def __init__(self):
        ''''''
        #self.model = Invoice
        self.status_code = 200
        self.response_message = 'OK' 
        self.response = {
            'res_data': {}
        }

    @decorator_4xx([])
    def dispatch(self, *args, **kwargs):
        super(self.__class__, self).dispatch(*args, **kwargs)
        # if self.status_code == 200:
        #     seialized = self.model.objects.serializer(query_set)
        #     self.response['res_data'] = seialized
        return JsonResponse(self.response, status=self.status_code)

    def post(self, request, *args, **kwargs):
        from Indent.models import Indent

        #0 -Monday, 1 -Tuesday, 2-Wed, 3-Thrus, 4-Friday, 5 - Satureday, 6-Sunday
        self.status_code = 201
        params = json.loads(request.body)
        _area_id = params.get('area_id')
        _publisher_id = params.get('publisher_id')

        #import pdb; pdb.set_trace()
        vendors = Vendor.objects.filter(area__id=_area_id)

        try:
            _publisher = Publisher.objects.get(pk=_publisher_id)
            query = {
                'vendor__in': vendors,
                'status': False,
                'publisher':_publisher,
            }
            if 'from' in params.keys():
                query['date__gte'] = params.get('from')
            if 'to' in params.keys():
                query['date__lte'] = params.get('to')
            _indents = Indent.objects.filter(**query).order_by('-date')
            vendors_bill = dict()
            with transaction.atomic():
                for indent in _indents:
                    try:
                        Transaction.objects.get(txn_type='BILLED', indent=indent)
                    except Transaction.DoesNotExist as ex:
                        _balance = Balance.objects.get(vendor=indent.vendor)
                        _price = Price.objects.get(status=True,\
                                                   day=indent.date.weekday(),\
                                                   publisher=_publisher)

                        amount = indent.indent * _price.selling_price
                        _balance.runningvalue += amount
                        indent.status = True

                        txn = Transaction(vendor=indent.vendor, amount=amount, txn_type='BILLED',\
                                          txn_reason=str(indent.date), indent=indent, 
                                          previous_balance=_balance.runningvalue)
                        txn.save()
                        indent.save()
                        _balance.save()
        except Publisher.DoesNotExist as ex:
            self.status_code = 400
            raise AssertionError('Unable to find Publisher')  
        except AssertionError as ex:
            self.status_code = 400
        except Exception as ex:
            print str(ex)
        return list()

class Payment(View):
    ''''''
    def __init__(self):
        ''''''
        #self.model = Invoice
        self.status_code = 201
        self.response_message = 'OK' 
        self.response = {
            'res_data': {}
        }

    @decorator_4xx([])
    def dispatch(self, *args, **kwargs):
        super(self.__class__, self).dispatch(*args, **kwargs)
        return JsonResponse(self.response, status=self.status_code)

    def post(self, request, *args, **kwargs):
        params = json.loads(request.body)
        cid = params.get('cid')
        amount = float(params.get('amount'))
        _vendor_id = params.get('vendor_id')
        try:
            _vendor = Vendor.objects.get(pk=_vendor_id)
            with transaction.atomic():
                txn = Transaction(amount=amount, vendor=_vendor, txn_type='PAID', user_id=cid)
                balance = Balance.objects.get(vendor=_vendor)
                balance.runningvalue -= amount
                txn.save()
                balance.save()
        except Vendor.DoesNotExist as ex:
            self.status_code = 400
        except AssertionError as ex:
            self.status_code = 400

        return list()

class TransactionsAPI(View):
    ''''''
    def __init__(self):
        ''''''
        self.model = Transaction
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
        vendor_id = params.get('vendor_id')
        query = {
            'vendor_id': vendor_id,
        }

        transactions = Transaction.objects.filter(**query)
        return transactions

class BalanceAPI(View):
    def __init__(self):
        ''''''
        self.model = Balance
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
        _area_id = params.get('area_id')
        _vendors_balance = Balance.objects.select_related('vendor').filter(vendor__area_id=_area_id)
        return _vendors_balance


#class HardCopyGenerateBill(View):
