from csv import list_dialects
from django.contrib import admin

# Register your models here.

from .models import *
class Order_plan_detailsAdmin(admin.ModelAdmin):
    list_display = ['id','fee_title','datetime','name','email','mobile','amount','razorpay_payment_id','payment_uuid','received_other_source','is_active']
admin.site.register(Order_plan_details,Order_plan_detailsAdmin)