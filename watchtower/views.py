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

SQL_TEMPLATE_WHERE = Template("""SELECT $search_columns
FROM sys_info
WHERE $criteria;""")

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

        column_sql = ""
        criteria = ""

        first_iter = True
        for key, value in a:
            if rest_dict.has_key(key.lower()):
                # Handle daterange as a special case
                if (key == "daterange"):
                    # Assumes times are in the format "start-stop" in milliseconds
                    times = value.split('-')
                    criteria = "Timestamp BETWEEN %s AND %s" % (times[0], times[1])
                # Stop searching through query string if all is encountered
                elif(key == "all"):
                    column_sql = "*"
                    break
                else:
                    if first_iter:
                        column_sql += rest_dict[key]
                        first_iter = False
                    else:
                        column_sql += "," + rest_dict[key]
        result = ""
        if column_sql:
            result = self.query_database(column_sql, criteria)
        return ("Query:[%s] Result: %s" % (column_sql, str(result)), 200)

    def convert_to_json(self, search_columns, results):
        json_string = ""
        if(search_columns == "*"):
            pass
        else:
            for row in results:
                pass



    def query_database(self, search_columns, criteria=0):
        ''' performs the query on the database'''
        c = db_conn.cursor()
        if criteria:
            c.execute(SQL_TEMPLATE_WHERE.substitute({"search_columns": search_columns, "criteria":criteria}))
            results = c.fetchall()
        else:
            c.execute(SQL_TEMPLATE.substitute({"search_columns":search_columns}))
            results = c.fetchone()
        # TODO - self.convert_to_json(search_columns, results)
        return results
