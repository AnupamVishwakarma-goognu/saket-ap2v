from django.http import HttpResponse
import random, string
from captcha.image import ImageCaptcha

def captcha_create(request):
    string_data = ''.join(random.choice(string.digits) for _ in range(4))
    request.session['session_captcha_code'] = string_data
    make_image = ImageCaptcha(fonts=['/opt/projects/ap2vnoida/ap2v/monofont.ttf'])
    image = make_image.generate(string_data)
    response = HttpResponse(image, content_type = "image/png")
    return response
