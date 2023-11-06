from django.shortcuts import render
from ems.models import *
from django.http import HttpResponseRedirect

# timezone

def index(request):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/ems/main/'))
    return response

def change_theme(request, **kwargs):
    if 'dark_mode' in request.COOKIES:
        dark_mode = not bool(request.COOKIES['dark_mode'])
    else:
        dark_mode = True

    response = HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    if dark_mode:
        response.set_cookie('dark_mode', '1', max_age=31536000)  # 쿠키를 설정하고 1년(31536000초) 동안 유지합니다
    else:
        response.delete_cookie('dark_mode')

    return response