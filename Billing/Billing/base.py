
from django.db import models

class BaseModel(models.Model):
	created_on = models.DateTimeField(auto_now_add = True, db_index=True, \
									verbose_name='created_on', null=True, blank=True)
	updated_on = models.DateTimeField(auto_now = True, db_index=True, \
									verbose_name='updated_on', null=True, blank=True)
	is_deleted = models.BooleanField(default=False, verbose_name='deleted')

	class Meta:
		abstract = True