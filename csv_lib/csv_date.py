"""
CSV Utilities Date Module
csv_date.py
Rawser Spicer
created: 2014/02/06
modified: 2014/02/07

        This module handles datetime objects for the csv_lib library. It       
    includes the following functions:
        string_to_datetime      -- converts a stirng to a datetime 
                                   object        
        get_last_date           -- get the last date in a file  
        make_interval           -- makes a date time interval tuple
        is_in_interval          -- checks if a date is in an interval

    version 2014.2.7.1
        added get_last_date function. updated make_interval to accept datetime
    objects as well as strings. added header documentation
    
    version 2014.2.6.1
        initial version functions unchanged from csv_plot.py
"""
import datetime
import re
from csv_lib.csv_utilities import print_center, exit_on_failure


def string_to_datetime(string):
    """
    converts a string to a datetime object
    string = the string to convert
    returns a date time date
    """
    reg_exp = r'^"*(\d+)-(\d+)-(\d+) *(\d+)*:*(\d+)*:*(\d+)*"*$'
    try:
       
        ts_numbers = [t(s) for t , s in zip((int, int, int, int, int, int),
                                        re.search(reg_exp,string).groups())]
        temp = datetime.datetime(ts_numbers[0], ts_numbers[1], 
                                     ts_numbers[2], ts_numbers[3], 
                                     ts_numbers[4], ts_numbers[5])
    except TypeError:
        ts_numbers = [t(s) for t , s in zip((int, int, int), 
                                        re.search(reg_exp,string).groups())]
        temp = datetime.datetime(ts_numbers[0], ts_numbers[1], ts_numbers[2])   
    return temp


def get_last_date(f_name):
    """
    gets the last date form a file
    f_name = the name of the file
    returns a datetime date
    """
    try:
        f_stream = open(f_name, 'r')
    except IOError:
        string = "ERROR: could not read file " + f_name
        print_center(string,'*')
        exit_on_failure()
    
    f_stream.readline()             # Read the first line.
    f_stream.seek(-2, 2)            # Jump to the second last byte.
    
    while f_stream.read(1) != "\n": # Until EOL is found...
        f_stream.seek(-2, 1)        # ...jump back the read byte plus one more.
    last = f_stream.readline()

    return string_to_datetime(last.split(',')[0])


def make_interval(start, end):
    """
    makes a datetime interval from date strings that is a two value tuple
    start = a string, or datetime object of the start date
    end = a string, or datetime object of the end date
    returns a date time interval A tuple of (start,end)
    """
    try:
        start = string_to_datetime(start)
    except AttributeError:
        start = datetime.datetime.min
    except TypeError:
        start = start

    try:
        end = string_to_datetime(end)
    except AttributeError:
        end = datetime.datetime.max
    except TypeError:
        end = end
    
    interval = (start, end)
    return interval


def is_in_interval(date, interval):
    """
    is the date in the interval
    date = a date
    interval = an interval of dates
    returns true if date is in the give interval
    """
    return (interval[0] <= date and date <= interval[1])

