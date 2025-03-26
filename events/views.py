from django.shortcuts import render
from .models import Events 
from .models import Venue
from home.models import Configrations
from django.conf import settings

live_configration_id = settings.LIVE_CONFIGRATION_ID
# Create your views here.

def all_events(request):
	configration = Configrations.objects.get(id=live_configration_id)
	header_text = configration.events_header_text
	events = Events.objects.order_by('date')
	#venues = Venue.objects.order_by('name')
	return render(request, 'events/all_events.html', {'events':events, "header_text": header_text})

def events(request):
	ctx={}
	events_obj = Events.objects.all()
	ctx['events']=events_obj
 
	return render(request, 'events/events.html', ctx)
