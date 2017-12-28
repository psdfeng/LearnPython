# -*- coding: utf-8 -*-

from django.http import HttpResponse

def hello(request):
    return HttpResponse("<p>世界好</p>")
