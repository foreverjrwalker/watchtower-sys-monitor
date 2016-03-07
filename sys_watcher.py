#!/usr/bin/env python
# encoding: utf-8
'''
*#############################################################################
Created on Mar 6 2016

@author: slaugms
'''

from __future__ import print_function
from _collections import deque
from sys import platform as _platform
import threading
import subprocess
import datetime
import inspect  # Debug Information
import pprint
import sqlite3
import sys
from time import sleep
from time import time

import psutil as PS

EXECUTING = 0
UPDATE_RATE = 1

# Main program
current_network_throughput = deque(maxlen=1)
VERBOSE = 1

def exit_cleanly(message=""):
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    writeout("Exiting from: %s - %s " % (calframe[1][3], message)) 
    sys.exit(1);

# Find and replace commands from the argument list
def fill_arguments(command, argumentList):
    if command is not None and isinstance(command, basestring):
        for argument in argumentList:
            command = command.replace(argument[0], argument[1])
    return command

def get_timestamp():
    return  datetime.datetime.now().strftime("%b-%d %Y %H:%M:%S")

def start_monitoring():
    # Start the Network Thread
    start_network_thread()
    # Connect to database
    conn = connect_to_database("sysinfo.db.sqlite3")

    while (EXECUTING):
        # Update the message
        current_state = retrieve_current_system_state()
        pprint.pprint(current_state)
        update_database(current_state, conn)
        sleep(UPDATE_RATE)
    return True

def start_network_thread():
    # Launch Network speed calculation daemon
    mythread = threading.Thread(target=calculate_network_speed,
                                args=(current_network_throughput,))
    mythread.daemon = True
    mythread.start()

def writeout(message, error=False):
    # Pretty print and time stamp output messages
    if (error):
        print(get_timestamp() + " " + message, file=sys.stderr)
    else:
        print(get_timestamp() + " " + message)

def connect_to_database(file_location):
    # Connecting to the Database File
    writeout("Creating Database: %s" % file_location)
    conn = sqlite3.connect('file_location')
    c = conn.cursor()
    c.execute("""
    CREATE TABLE if not exists `sys_info` (
    `id`    INTEGER PRIMARY KEY AUTOINCREMENT,
    `TimeStamp`    TEXT,
    `Hostname`    TEXT,
    `KernelVersion`    TEXT,
    `CpuNum`    TEXT,
    `CpuUtilization`    TEXT,
    `DiskFree`    TEXT,
    `DiskPercent`    TEXT,
    `DiskTotal`    TEXT,
    `DiskUsed`    TEXT,
    `NetBytesRecv`    TEXT,
    `NetBytesSent`    TEXT,
    `NetPacketsRecv`    TEXT,
    `NetPacketsSent`    TEXT,
    `RamAval`    TEXT,
    `RamPercent`    TEXT,
    `RamTotal`    TEXT
);""")
    conn.commit()
    return conn

def get_kernel_version():
    message = ""
    if _platform == "linux" or _platform == "linux2":
            message = subprocess.check_output(['uname', '-rs']).strip()
    return message.strip();

def get_hostname():
    message = ""
    if _platform == "linux" or _platform == "linux2":
        message = subprocess.check_output(['uname' , '-n'])
    return message.strip()

def retrieve_current_system_state():
    global TIME_STARTED
    global LAST_BYTES_SENT
    global LAST_BYTES_RECEIVED
    dd = {}

    # System Stats
    dd['Timestamp'] = get_timestamp()
    dd['Hostname'] = get_hostname()
    dd["KernelVersion"] = get_kernel_version()

    # Ram Stats
    mem = PS.virtual_memory()
    dd["RamTotal"] = str(mem.total)
    dd["RamAval"] = str(mem.available)
    dd["RamPercent"] = str(mem.percent)

    # Network Stats
    net = PS.net_io_counters(False)
    dd["NetBytesSent"] = str(get_network_throughput(0))
    dd["NetBytesRecv"] = str(get_network_throughput(1))
    dd["NetPacketsSent"] = str(net.packets_sent)
    dd["NetPacketsRecv"] = str(net.packets_recv)

    # Processor Utilization
    cpuList = PS.cpu_percent(.5, True)
    percentUsage = 0
    for index, core in enumerate(cpuList):
        percentUsage += core
    dd["CpuNum"] = len(cpuList)
    dd["CpuUtilization"] = str(percentUsage)

    # Disk Usage
    usage = PS.disk_usage("/")
    dd["DiskUsed"] = str(usage.used)
    dd["DiskPercent"] = str(usage.percent)
    dd["DiskFree"] = str(usage.free)
    dd["DiskTotal"] = str(usage.total)
    return dd

def update_database(values_dict, conn):
    c = conn.cursor()
    sql = "INSERT INTO sys_info "
    c.execute()
    pass


def calculate_network_speed(data_queue):
    start_time = time()
    counter = PS.net_io_counters()
    total = (counter.bytes_sent, counter.bytes_recv)
    while True:
        last_total = total
        sleep(1)  # Wait 1 second
        cur_time = time()
        counter = PS.net_io_counters()
        total = (counter.bytes_sent, counter.bytes_recv)
        upload, download = [(now - last) / (cur_time - start_time) for now, last in zip(total, last_total)]
        data_queue.append((upload, download))
        start_time = time()

def get_network_throughput(num):
    output = 0
    try:
        if (num == 1 or num == 0):
            output = current_network_throughput[-1][num]
    except:
        output = 0
    return int(round(output))


def main(argv=None):
        global VERBOSE
        global EXECUTING
        if argv is None:
            argv = sys.argv
        else:
            sys.argv.extend(argv)
        try:
            VERBOSE = True
            writeout("######################################")
            writeout("         sys_watcher     ")
            writeout("######################################")
            if VERBOSE > 0:
                writeout("Verbose mode on")
            # Launch Monitoring Services
            if VERBOSE > 0:
                writeout("Launching Monitoring Services...")
            EXECUTING = 1
            if not start_monitoring():
                return writeout("StartServices (NTD) failed to start some service(s)")
            # Considerations - Error handling/Correction/Restart
            if VERBOSE > 0:
                writeout("Exiting...")
            return exit_cleanly("Program Complete!")

        except KeyboardInterrupt:
            ### handle keyboard interrupt ###
            sys.stderr.write("Received Keyboard interrupt, exiting...")
            return 0
        except Exception, e:
            raise(e)
            return 2


# Main Function
if __name__ == "__main__":
    sys.exit(main())
