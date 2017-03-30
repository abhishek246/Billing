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