from __future__ import unicode_literals

from django.db import models

from Billing.base import BaseModel
from django.db.models import QuerySet
# Create your models here

class AreaManager(models.Manager):
    ''''''
    def from_serializeing_dict(self, model_object):
        _serializeing_dict = {
                'area': model_object.area,
                'id': model_object.pk,
                'verbose_name': model_object.verbose_name
            }
        return _serializeing_dict

    def serializer(self, query_set):
        #import pdb; pdb.set_trace()
        serialized = None
        if isinstance(query_set, list) or isinstance(query_set, QuerySet):
            _serializeing_list = list()
            for model_object in query_set:
                _serializeing_list.append(self.from_serializeing_dict(model_object))
            serialized ={'areas': _serializeing_list}
        else:
            serialized = self.from_serializeing_dict(query_set)
        return serialized


class Area(BaseModel):
    ''''''

    area = models.CharField(max_length=255)
    verbose_name = models.CharField(max_length=255)
    status = models.SmallIntegerField(default=0)

    objects = AreaManager()

    class Meta:
        db_table = 'area'
        verbose_name = 'area'
        verbose_name_plural = 'areas'

    def __unicode__(self):
        return  'Area Name: {0}'.format(str(self.area))