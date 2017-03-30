from django.contrib import admin
from .models import *

class page_list(admin.ModelAdmin):
	list_per_page = 1000

admin.site.register(Publisher)
admin.site.register(Indent)