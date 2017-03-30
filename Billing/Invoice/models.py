from __future__ import unicode_literals

from django.db import models
from django.db.models import QuerySet
    
from Billing.base import BaseModel
from Indent.models import Publisher, Indent
from Vendors.models import Vendor
#import Vendor as Vm
# Create your models here.
class TransactionManager(models.Manager):
    ''''''
    def from_serializeing_dict(self, model_object):
        _serializeing_dict = {
                'amount': model_object.amount,
                'copies': None,
                'taken_date': None,
                'txn_type': model_object.txn_type,
                'txn_reason': model_object.txn_reason,
                'user_id': model_object.user_id,
            }
        if model_object.indent:
            _serializeing_dict['copies'] = model_object.indent.indent
            _serializeing_dict['taken_date'] = model_object.indent.date
        return _serializeing_dict

    def serializer(self, query_set):
        #import pdb; pdb.set_trace()
        serialized = None
        if isinstance(query_set, list) or isinstance(query_set, QuerySet):
            _serializeing_list = list()
            for model_object in query_set:
                _serializeing_list.append(self.from_serializeing_dict(model_object))
            serialized ={'txns': _serializeing_list}
        else:
            serialized = self.from_serializeing_dict(query_set)
        return serialized

class BalanceManager(models.Manager):
    ''''''
    def from_serializeing_dict(self, model_object):
        _serializeing_dict = {
                'amount': str(model_object.runningvalue),
                'vendor_name': model_object.vendor.name,
                'vendor_abbv': model_object.vendor.abbrivation,
                'vendor_id': model_object.vendor.pk 
            }
        return _serializeing_dict

    def serializer(self, query_set):
        #import pdb; pdb.set_trace()
        serialized = None
        if isinstance(query_set, list) or isinstance(query_set, QuerySet):
            _serializeing_list = list()
            for model_object in query_set:
                _serializeing_list.append(self.from_serializeing_dict(model_object))
            serialized ={'vendors': _serializeing_list}
        else:
            serialized = self.from_serializeing_dict(query_set)
        return serialized

class Price(BaseModel):
    publisher = models.ForeignKey(Publisher)
    selling_price = models.FloatField() 
    original_price = models.FloatField()
    status = models.BooleanField(default=True)
    day = models.CharField(max_length=255)

    def __unicode__(self):
        return '{0}: {1} -- {2}'.format(self.publisher.abbrivation, self.selling_price, self.day)

    class Meta:
        db_table = 'price'
        verbose_name = 'price'
        verbose_name_plural = 'price'

class Balance(BaseModel):
    runningvalue = models.FloatField()
    vendor = models.OneToOneField(Vendor, related_name='vendor_balance')

    objects = BalanceManager()
    def __unicode__(self):
         return '{0}: {1}'.format(self.vendor.name, self.runningvalue)

    class Meta:
        db_table = 'balance'
        verbose_name = 'balance'
        verbose_name_plural = 'balance'

class Transaction(BaseModel):
    ''''''
    TXN_TYPE = (('B', 'BILLED'),
        ('P', 'PAID'))

    amount = models.FloatField()
    vendor = models.ForeignKey(Vendor, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    indent = models.ForeignKey(Indent, null=True, blank=True)
    txn_type = models.CharField(max_length =255)
    txn_reason = models.CharField(max_length=255)
    previous_balance = models.CharField(max_length=255)

    objects = TransactionManager()
    def __unicode__(self):
        return '{0} - {1} / {2}  : {3}'.format(self.vendor, self.txn_type, self.txn_reason, self.amount)

    class Meta:
        db_table = 'transaction'
        verbose_name = 'transaction'
        verbose_name_plural = 'transactions'
