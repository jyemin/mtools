from datetime import datetime
import time
from mtools.util.logline import LogLine
import os
from mtools.mplotqueries.plottypes import duration_type

storage_dir = "/tmp/mtools_storage" #TODO import this from app config


def extract_plotpoints(line):
    """ given a (parsed) log line, return an object
    that contains data we want to plot
    """
    #return time.mktime(line.datetime.timetuple()), line.duration, line.operation
    return time.mktime(datetime.now().timetuple()), line.duration, line.operation

def generate_plot_report(file_id):
    groupkey = "namespace" #operation
    plotter = duration_type.DurationPlotType()
    logfile = open(os.path.join(storage_dir, str(file_id)))

    report = {'groups':{}}

    i = 0
    for ll in logfile:
        i+= 1
        line = LogLine(ll)
        if plotter.accept_line(line):
            plotpoint = extract_plotpoints(line)
            group_val = getattr(line, groupkey)
            report['groups'].setdefault(group_val, list()).append(plotpoint)

    print i, "lines processed"

    
