from django.shortcuts import render
from django.http import HttpResponse
from .models import Text,Video
from home.models import Configrations
from django.conf import settings

# Create your views here.
#testimonials=Text.objects.all()

live_configration_id = settings.LIVE_CONFIGRATION_ID
configration = Configrations.objects.filter(id=live_configration_id)

def all_testimonials(request):
	testimonials=Text.objects.all().order_by('-date')
	testimonials_video=Video.objects.order_by('-date')
	return render(request,'testimonials/all_testimonials.html',{'testimonials':testimonials,'testimonials_video':testimonials_video})#, "header_text": configration.testimonials_header_text})
