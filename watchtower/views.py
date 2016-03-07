from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views.generic.base import View
import json
import sqlite3
import os
from string import Template

# Template for Selecting from data base
SQL_TEMPLATE = Template("""SELECT $search_columns
FROM sys_info;""")

# Rest command dictionary for lookup
rest_dict = {'all': "*",
             'cpuinfo': "cpunum, cpuutilization",
             'netinfo': "netbytesrecv,netbytessent,netpacketsrecv,netpacketssent",
             'raminfo': "ramaval,rampercent,ramtotal",
             'diskinfo': "disktotal,diskused,diskfree,diskpercent",
             'hostinfo': "hostname, kernelversion",
             'cpunum': "cpunum",
             'cpuutilization': "cputilization",
             'diskpercent': "diskpercent",
             'diskfree': "diskfree",
             'disktotal': "disktotal",
             'diskused': "diskused",
             'hostname': "hostname",
             'kernelversion': "kernelversion",
             'netbytesrecv': "netbytesrecv",
             'netbytessent': "netbytessent",
             'netpacketsrecv': "netpacketsrecv",
             'netpacketssent': "netpacketssent",
             'ramaval': "ramaval",
             'rampercent': "rampercent",
             'ramtotal': "ramtotal"}

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

        # List comprehension for enumerating values in the query string
        a = (param.split("=") for param in query_string.split('&'))
        sql = ""
        first_iter = True
        for key, value in a:
            if rest_dict.has_key(key.lower()):
                # Handle daterange as a special case
                if (key == "daterange"):
                    raise NotImplemented

                # Stop searching through query string if all is encountered
                elif(key == "all"):
                    sql = "*"
                    break
                else:
                    if first_iter:
                        sql += rest_dict[key]
                        first_iter = False
                    else:
                        sql += "," + rest_dict[key]

        result = ""
        if sql:
             result = self.query_database(sql, None)
        return ("Query:[%s] Result: %s" % (sql,str(result)) , 200)

    def convert_to_json(self, value_string):
        pass

    def convert_date_to_milliseconds(self, d):
        ''' This method will take in values from the get string (Year, Month Date,
         Hour Minutes and return the appropriate time in milliseconds 
         for comparison'''
        pass

    def query_database(self, query_string, return_format):
        ''' performs the query on the database'''
        c = db_conn.cursor()
        c.execute(SQL_TEMPLATE.substitute({"search_columns":query_string}))
        result = c.fetchone()
        return result
