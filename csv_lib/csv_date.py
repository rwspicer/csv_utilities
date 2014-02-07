"""
CSV date utilities module
csv_date.py
Rawser Spicer
created: 2014/02/06
modified: 2014/02/06

    version 2014.2.6.1
        inital version functions unchanged from csv_plot.py
"""
import datetime
import re

def string_to_datetime(string):
    """
    converts a string to a datetime object
    string = the string to convert
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


def make_interval(start, end):
    """
    makes a datetime interval from date strings that is a two value tuple
    start = a string of the start date
    end = a string of the end date
    returns an interval
    """
    try:
        start = string_to_datetime(start)
    except AttributeError:
        start = datetime.datetime.min
    
    try:
        end = string_to_datetime(end)
    except AttributeError:
        end = datetime.datetime.max
    
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
   
