from __future__ import unicode_literals

from django.db import models
from django.db.models import QuerySet

from Billing.base import BaseModel
from Areas.models import Area

# Create your models here.

class VendorManager(models.Manager):
    ''''''
    def from_serializeing_dict(self, model_object):
        from Invoice.models import Balance
        _balance = Balance.objects.get(vendor=model_object)
        _serializeing_dict = {
                'name': model_object.name,
                'mobile_number': model_object.mobile_number,
                'balance': _balance.runningvalue,
                'id': model_object.pk,
                'abbv': model_object.abbrivation
            }
        return _serializeing_dict

    def serializer(self, query_set):
        #import pdb; pdb.set_trace()
        serialized = None
        if isinstance(query_set, list) or isinstance(query_set, QuerySet):
            _serializeing_list = list()
            for model_object in query_set:
                _serializeing_list.append(self.from_serializeing_dict(model_object))
            serialized ={'daily_indent': _serializeing_list}
        else:
            serialized = self.from_serializeing_dict(query_set)
        return serialized


class Vendor(BaseModel):
    name = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=255, db_index=True, editable = True, unique=True)
    abbrivation = models.CharField(max_length=255, db_index=True, unique=True)
    area = models.ForeignKey(Area)

    objects = VendorManager()
    def __unicode__(self):
        return 'name: {0} {1}'.format(self.name, self.mobile_number)

    class Meta:
		db_table = 'vendor'
		verbose_name = 'vendor'
		verbose_name_plural = 'vendors'