from .models import Author
from .models import Configrations
from .models import Location
from .models import FeaturedCertifications
from .models import SidebarCategory
from django.contrib import admin
from .models import Category
class CategoryAdmin(admin.ModelAdmin):
    list_display =['id','name','slug','display_home','index']
admin.site.register(Category,CategoryAdmin)

from .models import Refer_and_Earn
class Refer_and_EarnAdmin(admin.ModelAdmin):
    list_display =['id','candidate_phone','candidate_exists','friend_name','friend_phone','friend_email','friend_designation']
admin.site.register(Refer_and_Earn,Refer_and_EarnAdmin)


admin.site.register(Author)
admin.site.register(SidebarCategory)
admin.site.register(Configrations)
admin.site.register(Location)
admin.site.register(FeaturedCertifications)
