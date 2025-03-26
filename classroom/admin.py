from django.contrib import admin
from .models import BatchStudentFeedback,StudyMaterial
from .models import ClassRoomCourseOffer
class BatchStudentFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id','datetime','user','batch','rating','comment']
admin.site.register(BatchStudentFeedback,BatchStudentFeedbackAdmin)


class ClassRoomCourseOfferAdmin(admin.ModelAdmin):
    list_display = ['id','discount','discount_valid_till','discount_after_date']
admin.site.register(ClassRoomCourseOffer,ClassRoomCourseOfferAdmin)


admin.site.register(StudyMaterial)