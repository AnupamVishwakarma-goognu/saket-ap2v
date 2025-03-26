from django.contrib import admin
from .models import *

class InstallmentsAdmin(admin.ModelAdmin):
    list_display = ['id','enrollmentid','payment_method','installment_no','installment','due_date','paid_unpaid','added_on','attachment','fee_type']
    list_filter = ['paid_unpaid','added_on']
admin.site.register(Installments,InstallmentsAdmin)

class EnrollmentsAdmin(admin.ModelAdmin):
    list_display = ['id','enquiry_course_id','payment_method','discussed_fee','registered_on','registered_by']
admin.site.register(Enrollments,EnrollmentsAdmin)

admin.site.register(PaymentMethod)
# admin.site.register(EnrollCourse)

from .models import PartnerPayment
class PartnerPaymentAdmin(admin.ModelAdmin):
    list_display = ['id','partner','enrollment','amount','is_paid','paid_on','added_on','added_by','updated_by']
admin.site.register(PartnerPayment,PartnerPaymentAdmin)

from .models import SharedBooks
class SharedBooksAdmin(admin.ModelAdmin):
    list_display = ['id','enrollments','book','is_shared','shared_on']
admin.site.register(SharedBooks,SharedBooksAdmin)