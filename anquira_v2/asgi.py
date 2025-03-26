import os
#from django.core.asgi import get_asgi_application
import django
from channels.layers import get_channel_layer
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anquira_v2.settings')

django.setup()

#application = get_channel_layer()
application = get_default_application()

