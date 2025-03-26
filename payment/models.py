from statistics import mode
from django.db import models
import uuid

# Create your models here.
class Order_plan_details(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    name = models.CharField(max_length=250, null=False, blank=False)
    email = models.CharField(max_length=250, null=False, blank=False)
    mobile = models.CharField(max_length=20, null=False, blank=False)
    amount = models.CharField(max_length=250, null=False, blank=False)
    order_id = models.CharField(max_length=255,null=True,blank=True)
    payment_status = models.BooleanField(null=True, blank=True, default=False)
    razorpay_payment_id = models.CharField(max_length=255,null=True,blank=True)
    razorpay_order_id = models.CharField(max_length=255,null=True,blank=True)
    razorpay_signature = models.CharField(max_length=255,null=True,blank=True)
    razerpay_order_obj = models.TextField(null=True, blank=True, default=None)
    payment_uuid = models.UUIDField(default=uuid.uuid4, null=False, blank=False)
    fee_title = models.CharField(max_length=250, null=True, blank=True, default=False)
    received_other_source = models.BooleanField(default=False, null=True, blank=True)
    received_other_source_detail = models.TextField(null=True, blank=True, default=None)
    is_active = models.BooleanField(default=True, null=True, blank= True)

    def payment_status(self):
        if self.razorpay_signature:
            return "Success"
        return "Failed"