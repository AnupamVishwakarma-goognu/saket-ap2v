#!/bin/bash
#

cd /opt/projects/anquira

/opt/py3_vitualenv/dj3_anquira/bin/python manage.py batch_recording_url
/opt/py3_vitualenv/dj3_anquira/bin/python manage.py download_recording
