from datetime import datetime
import time
from mtools.util.logline import LogLine
import os
from mtools.mplotqueries.plottypes import duration_type
from pymongo import MongoClient
from collections import OrderedDict

db = MongoClient().files



storage_dir = "/tmp/mtools_storage" #TODO import this from app config


def extract_plotpoints(line):
    """ given a (parsed) log line, return an object
    that contains data we want to plot
    """
    #return time.mktime(line.datetime.timetuple()), line.duration, line.operation
    return time.mktime(datetime.now().timetuple()), line.duration, line.operation

def generate_plot_report(file_id, task_id):
    groupkey = "namespace" #operation
    plotter = duration_type.DurationPlotType()
    logfile = open(os.path.join(storage_dir, str(file_id)))

    names_keyspaces = {}
    keyspaces = []
    report = {'groups':keyspaces} # [{namespace:'ns1',points:[]}

    i = 0
    for ll in logfile:
        i+= 1
        line = LogLine(ll)
        if plotter.accept_line(line):
            plotpoint = extract_plotpoints(line)
            group_val = getattr(line, groupkey)
            
            group_index = names_keyspaces.get(group_val,None)
            if not group_index:
                keyspaces.append(group_val)
                names_keyspaces[group_val] = len(keyspaces)
                group_index = len(keyspaces)
                report['groups'].append({'groupkey':group_val,'points':[]})

            report['groups'][group_index]['points'].append(plotpoint)

    report['_id'] = str(file_id) + "_" + "durationplot"
    db.reports.update({"_id":report['_id']}, report, upsert=True)
    #print i, "lines processed"

    
