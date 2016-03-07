from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.base import View

def index(request):
    return HttpResponse("Hello, World!")

class WatchtowerView(View):
    ''' This is the primary view for the REST-ful API '''
    def get(self, request):
        # Get the query string from the request and change it to 
        # lower case it for comparison reasons returns a tuple of message
        # and the response code 
        response = self.parse_query_string(request.GET.urlencode().lower())
        if response:
            pass
        return HttpResponse(response[0], status=response[1])
    
    def parse_query_string(self, query_string):
        items = query_string.split('&')
        return (str(items),200)
        pass
    
    def query_database(self):
        pass 