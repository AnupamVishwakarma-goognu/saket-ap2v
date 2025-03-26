from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from home.models import Configrations
from django.conf import settings

live_configration_id = settings.LIVE_CONFIGRATION_ID
configration = Configrations.objects.filter(id=live_configration_id)

def gallery(request):
	images=Gallery.objects.all()
	return render(request,'gallery/gallery.html',{'images':images})#, "header_text": configration.gallary_header_text})
