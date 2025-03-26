from django.contrib import admin
from .models import *

# Register your models here.


class BlogsAdmin(admin.ModelAdmin):
    list_display = ['id','title','city','categories','published_on','show_on_site','views']
admin.site.register(Blogs,BlogsAdmin)
admin.site.register(Comments)

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['id','date','type','index','question_title','question']
admin.site.register(QuestionAnswer,QuestionAnswerAdmin)

class InterviewQuestionTitleDescriptionAdmin(admin.ModelAdmin):
    list_display = ['id','title','slug','content','tags','categories','image']
admin.site.register(InterviewQuestionTitleDescription,InterviewQuestionTitleDescriptionAdmin)