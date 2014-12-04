"""
CSV Utilities Date Module
csv_date.py
Rawser Spicer
created: 2014/02/06
modified: 2014/12/04

        This module handles datetime objects for the csv_lib library. It       
    includes the following functions:
        string_to_datetime      -- converts a stirng to a datetime 
                                   object        
        get_last_date           -- get the last date in a file  
        make_interval           -- makes a date time interval tuple
        is_in_interval          -- checks if a date is in an interval

    
    version 2014.12.4.1:
        pads time in julian to datetime with extra zeros if its length is 1
    
    version 2014.12.1.2:
        updated the make interval excptions for the new string_to_datetime 
    method
   
    version 2014.12.1.1:
        updated string_to_datetime to use strptime in stead of re
   
    version 2014.11.17.1:
        there was extra 1 being added to the julian day, its not anymore

    version 2014.9.8.1:
        added support for string or int arguments to julian to datetime
    function, fixed 24 to 0 hour error, and fixed hhmm len error

    version 2014.8.29.1:
        updated the string to datetime function to handle string with 
    micro seconds
   
    version 2014.8.26.1:
        added julian_to_datetime function
   
    version 2014.8.8.1:
        updated documentataion
    
    version 2014.2.19.1
        fixed imports   

    version 2014.2.7.1
        added get_last_date function. updated make_interval to accept datetime
    objects as well as strings. added header documentation
    
    version 2014.2.6.1
        initial version functions unchanged from csv_plot.py
"""
import datetime
#import re
#from csv_lib.csv_utilities import print_center, exit_on_failure
import csv_utilities as csvu

def string_to_datetime(string):
    """
        converts a string to a datetime object
        
    arguments:
        string:     (string)the string to convert
    
    returns:
        a date time date
    """
    string = string.replace('"', "")
    strptime = datetime.datetime.strptime
    try:
        temp = strptime(string, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        try:
            temp = strptime(string, "%Y-%m-%d %H:%M:%S")
        except ValueError:
                temp = strptime(string, "%Y-%m-%d")
   
   
   
    #~ reg_exp = r'^"*(\d+)-(\d+)-(\d+) *(\d+)*:*(\d+)*:*(\d+)*.(\d+)*"*$'
    
    
    #~ try:
        #~ ts_numbers = [t(s) for t , s in zip((int, int, int, int, int, int, int),
                                        #~ re.search(reg_exp,string).groups())]
        #~ temp = datetime.datetime(ts_numbers[0], ts_numbers[1], 
                                 #~ ts_numbers[2], ts_numbers[3], 
                                 #~ ts_numbers[4], ts_numbers[5], ts_numbers[6])
    #~ except TypeError:
        #~ try:
            #~ reg_exp = r'^"*(\d+)-(\d+)-(\d+) *(\d+)*:*(\d+)*:*(\d+)*"*$'
            #~ ts_numbers = [t(s) for t , s in zip((int, int, int, int, int, int),
                                        #~ re.search(reg_exp,string).groups())]
            #~ temp = datetime.datetime(ts_numbers[0], ts_numbers[1], 
                                     #~ ts_numbers[2], ts_numbers[3], 
                                     #~ ts_numbers[4], ts_numbers[5])
        #~ except TypeError:
            #~ ts_numbers = [t(s) for t , s in zip((int, int, int), 
                                        #~ re.search(reg_exp,string).groups())]
            #~ temp = datetime.datetime(ts_numbers[0], ts_numbers[1],
                                                    #~ ts_numbers[2])
   
    return temp


def get_last_date(f_name):
    """
        gets the last date form a file
        
    arguments:    
        f_name:     (string) the name of the file
    
    returns:
        a datetime date
    """
    try:
        f_stream = open(f_name, 'r')
    except IOError:
        string = "ERROR: could not read file " + f_name
        csvu.print_center(string,'*')
        csvu.exit_on_failure()
    
    f_stream.readline()             # Read the first line.
    f_stream.seek(-2, 2)            # Jump to the second last byte.
    
    while f_stream.read(1) != "\n": # Until EOL is found...
        f_stream.seek(-2, 1)        # ...jump back the read byte plus one more.
    last = f_stream.readline()

    return string_to_datetime(last.split(',')[0])


def make_interval(start, end):
    """
        makes a datetime interval from date strings that is a two value tuple
    
    arguments:
        start:  (string| datetime) object of the start date
        end:    (string| datetime) object of the end date
    
    returns:
        a date time interval A tuple of (start,end)
    """
    try:
        start = string_to_datetime(start)
    except ValueError:
        start = datetime.datetime.min
    except TypeError:
        start = start

    try:
        end = string_to_datetime(end)
    except ValueError:
        end = datetime.datetime.max
    except TypeError:
        end = end
    
    interval = (start, end)
    return interval


def is_in_interval(date, interval):
    """
        is the date in the interval
    
    arguments:
        date:   (datetime) a date
        interval:   (datetime)pair an interval of dates
    
    returns:
        true if date is in the give interval
    """
    return (interval[0] <= date and date < interval[1])
    

def julian_to_datetime(year, day, hhmm):
    """
        coverts from a julian date to a date time 
        need to add hour
    """
    
    if len(hhmm) == 3:
        hhmm = "0" + hhmm
    elif len(hhmm) == 2:
        hhmm = "00" + hhmm
    elif len(hhmm) == 1:
        hhmm =  "000" + hhmm
 
    if int(hhmm[:2]) == 24:
        hhmm = "00" +  hhmm[2:]
        day = int(day) + 1

    basedate = datetime.datetime(int(year), 1, 1,
                                 int(hhmm[:2]), int(hhmm[2:]))
    return basedate + datetime.timedelta(int(day) - 1) 

