from django.contrib import admin
from .models import *

@admin.register(HealthProduct)
class HealthProductadmin(admin.ModelAdmin):
    list_display=['id','name','image','productprice','productquantity','offer']


@admin.register(Transaction)
class HealthProductadmin(admin.ModelAdmin):
    list_display=['id','user','category','category_id','purchase_quan','date']