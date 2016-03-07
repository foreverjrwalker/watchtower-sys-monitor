from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.base import View
import json
import sqlite3
import os

# Determine the absolute path to the system info database
dir_path = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
db_path = os.path.join(dir_path, "data/sysinfo.db.sqlite3")
db_conn = sqlite3.connect(db_path)


def index(request):
    return HttpResponse("Hello, World!")

class WatchtowerView(View):
    ''' This is the primary view for the REST-ful API '''
    def get(self, request):
        ''' Get the query string from the request and change it to 
         lower case it for comparison reasons returns a tuple of message
         and the response code''' 
        response = self.parse_query_string(request.GET.urlencode().lower())
        if response:
            pass
        return HttpResponse(response[0], status=response[1])

    def parse_query_string(self, query_string):
        ''' This method will parse the query string and return a tuple of the 
        the database values (in JSON) and the result code'''
        items = query_string.split('&')


        output = self.query_database(query_string)
        return (output, 200)
        
    def convert_to_json(self, value_string):
        pass
    
    def convert_date_to_milliseconds(self, d):
        ''' This method will take in values from the get string (Year, Month Date,
         Hour Minutes and return the appropriate time in milliseconds 
         for comparison'''
        pass

    def query_database(self, query_string):
        ''' performs the query on the database'''
        c = db_conn.cursor()
        c.execute("SELECT * FROM sys_info")

        pass 
