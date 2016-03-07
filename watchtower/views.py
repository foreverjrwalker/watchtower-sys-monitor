from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.base import View

def index(request):
    return HttpResponse("Hello, World!")


class WatchtowerView(View):
    ''' This is the primary view for the REST-ful API '''
    def get(self, request):
        return HttpResponse(str(request))
