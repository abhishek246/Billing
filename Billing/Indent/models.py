from __future__ import unicode_literals

from django.db import models

from django.db.models import QuerySet
# Create your models here.
from Billing.base import BaseModel
from Vendors.models import Vendor

class IndentManager(models.Manager):
    ''''''
    def from_serializeing_dict(self, model_object):
        _serializeing_dict = {
                'indent': model_object.indent,
                'date': str(model_object.date),
                #'': model_object.verbose_name
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


class PublisherManager(models.Manager):
    ''''''
    def from_serializeing_dict(self, model_object):
        _serializeing_dict = {
                'name': model_object.name,
                'abbv': model_object.abbrivation,
                'id': model_object.pk
            }
        return _serializeing_dict

    def serializer(self, query_set):
        #import pdb; pdb.set_trace()
        serialized = None
        if isinstance(query_set, list) or isinstance(query_set, QuerySet):
            _serializeing_list = list()
            for model_object in query_set:
                _serializeing_list.append(self.from_serializeing_dict(model_object))
            serialized ={'publishers': _serializeing_list}
        else:
            serialized = self.from_serializeing_dict(query_set)
        return serialized


class Publisher(BaseModel):
    name = models.CharField(max_length=255)
    abbrivation = models.CharField(max_length=255, db_index=True)

    objects = PublisherManager()
    def __unicode__(self):
        return '{0}'.format(self.name)

    class Meta:
        db_table = 'publisher'
        verbose_name = 'publisher'
        verbose_name_plural = 'publishers'

class Indent(BaseModel):
    vendor = models.ForeignKey(Vendor)
    publisher = models.ForeignKey(Publisher)
    indent = models.IntegerField(default=0)
    date = models.DateField()
    status = models.BooleanField(default=False)

    objects = IndentManager()

    def __unicode__(self):
        return 'name: {0} {1}'.format(self.vendor, self.indent)

    class Meta:
        db_table = 'indent'
        verbose_name = 'indent'
        verbose_name_plural = 'indent'
        unique_together = (("vendor", "date"),)
