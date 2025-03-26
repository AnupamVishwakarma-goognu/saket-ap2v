As we have email addres instead of username for login. Hence, we need to change below files of Channels and Django-Chatter modules. The updated file placed in the same directory.

- /opt/py3env/anquira/lib/python3.6/site-packages/django_chatter/views.py
- /opt/py3env/anquira/lib/python3.6/site-packages/channels/layers.py


The version of above modules are:
channels==2.1.7
django-chatter==1.0.7

# -- start server commnad
daphne anquira.asgi:application --port 8000
