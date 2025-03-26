from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from users.views import logout

def custome_check():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            print(request.user.is_active)
            print("--------------------------------------------------------------")
            if request.user.is_active:
                return view_func(request, *args, **kwargs)
            else:
                if request.user.is_authenticated:
                    logout(request)
                    return HttpResponseRedirect("/")
                else:
                    return HttpResponseRedirect("/")
        return wrap
    return decorator