"""
version 2014.2.6.1
    this version of the plotting module supports graphing intervals

"""
import numpy
import sys
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook 
import datetime


def load_file_to_plot(f_name,skip = 4):
    """
    loads a array of a date time opject and an array of coorisponding values
    """    
    date_string , value = numpy.loadtxt(f_name, 
                    dtype = {'names':('date' , 'val'),'formats':('S100','f4')},
                    delimiter=',', usecols=(0 , 1), skiprows=skip, unpack=True)
    date = []
    for items in date_string:
        date.append(string_to_datetime(items))

    return date, value


def set_up_plot(title = "plot", x_axis = "x-axis", y_axis = "y-axis",
                                                    mode = "year"):

    fig, ax = plt.subplots()
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)

    if ("year" == mode):
        major   = mdates.MonthLocator()  
        major_fmt = mdates.DateFormatter('%b')
        minor = mdates.DayLocator(interval = 5)
    else: 
        major   = mdates.MonthLocator()  
        major_fmt = mdates.DateFormatter('%b')
        minor = mdates.DayLocator()
   
    ax.xaxis.set_major_locator(major)
    ax.xaxis.set_major_formatter(major_fmt)
    ax.xaxis.set_minor_locator(minor)
    fig.autofmt_xdate()


def show_plot():
    plt.show()  

def string_to_datetime(string):
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
        temp = datetime.datetime(ts_numbers[0],ts_numbers[1],ts_numbers[2])

    return temp

def make_interval(start, end):
    interval = (string_to_datetime(start), string_to_datetime(end))
    return interval


def is_in_interval(date, interval):
    return (interval[0] <= date and date <= interval[1])
        
  


def line_to_plot(interval,dates,vals):
    """
    gennerates a line to plot
    """
    b = []
    b_v = []
    index = 0 
    while (index < len(dates)):
        if ( is_in_interval(dates[index], interval)):
            temp = datetime.date(1000,dates[index].month,dates[index].day)
            b.append(temp)
            b_v.append(vals[index])
        index += 1
    return plt.plot(b,b_v)
