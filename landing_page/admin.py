from django.contrib import admin

# Register your models here.
from .models import Landing_Page
class Landing_PageAdmin(admin.ModelAdmin):
    list_display = ['pk','slug','title', 'description', 'overview', 'overview_point','skill_covered',
                    'advisor_number','anquira_reference','student_enrolled','duration','start_date','hiring_partners','price','emi','hours']
admin.site.register(Landing_Page,Landing_PageAdmin)


from .models import SoftwareTools
class SoftwareToolsAdmin(admin.ModelAdmin):
    list_display = ['pk','belong_landing_page', 'alt_text', 'image']
admin.site.register(SoftwareTools,SoftwareToolsAdmin)


from .models import ExamCertification
class ExamCertificationAdmin(admin.ModelAdmin):
    list_display = ['pk','belong_landing_page', 'exam_certification_title', 'description', 'exam_certification_image']
admin.site.register(ExamCertification,ExamCertificationAdmin)


from .models import Projects
class ProjectsAdmin(admin.ModelAdmin):
    list_display = ['pk','belong_landing_page', 'title', 'description']
admin.site.register(Projects,ProjectsAdmin)


from .models import Testimonial
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['pk','belong_landing_page', 'name', 'description', 'image']
admin.site.register(Testimonial,TestimonialAdmin)

from .models import LandingPageInstructors
class LandingPageInstructorsAdmin(admin.ModelAdmin):
    list_display = ['id','name','company','company_logo','designation','about_instructor']
admin.site.register(LandingPageInstructors,LandingPageInstructorsAdmin)