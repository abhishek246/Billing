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
from Billing.base import decorator_4xx, gen_password_hash


class AreaAPI(View):
    ''''''
    def __init__(self):
        ''''''
        self.model = Area
        self.status_code = 200
        self.response_message = 'OK' 
        self.response = {
            'res_data': {}
        }

    @decorator_4xx(['cid', 'token'])
    def dispatch(self, *args, **kwargs):
        query_set = super(self.__class__, self).dispatch(*args, **kwargs)
        if self.status_code == 200:
            seialized = self.model.objects.serializer(query_set)
            self.response['res_data'] = seialized
        return JsonResponse(self.response, status=200)

    def get(self, request, *args, **kwargs):
        params = request.GET
        if params.get('area'):
            try:
                areas = Area.objects.get(pk=params.get('area'))
            except Area.DoesNotExists as ex:
                self.status = 400
                self.response_message = str(ex)
        else:
            areas = Area.objects.all()
    	return areas

class UserAPI(View):
    ''''''
    def __init__(self):
        ''''''
        self.model = Area
        self.status_code = 200
        self.response_message = 'OK' 
        self.response = {
            'res_data': {}
        }

    def dispatch(self, *args, **kwargs):
        return super(self.__class__, self).dispatch(*args, **kwargs)
        #if self.status_code == 200:
        ##    seialized = self.model.objects.serializer(query_set)
        #    self.response['res_data'] = seialized
        #return JsonResponse(self.response, status=200)

    def post(self, request, *args, **kwargs):
        params = json.loads(request.body)
        user = User.objects.get(pk = params.get('mobile_number'))
        if parmas.get('password') == user.password:
            self.response['res_data']['cid'] = user.pk
            self.response['res_data']['token'] = user.token
        else:
            self.response['res_data'] = dict()
        return JsonResponse(self.response, status=200)