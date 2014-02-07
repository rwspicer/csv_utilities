"""
CSV Utilitys Plot Module
csv_plot.py
Rawser Spicer
2014/02/06

    this module contains the ploting functions for csv_utilites 

version 2014.2.6.2
        updated all current function help string and moved datetime 
    related functions to csv_date

version 2014.2.6.1
        this version of the plotting module supports graphing intervals

"""
import numpy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from csv_lib.csv_date import string_to_datetime, is_in_interval
import datetime

def load_file_to_plot(f_name, skip = 4):
    """
        loads a array of a datetime.datetime object and an array of 
    coorisponding values
    
    f_name = the file name
    skip = number of rows to skip (defaluts to 4 the data logger header length)
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
    """
    sets up the plot labels
    title = the plots title
    x_axis = name of the x-axis
    y_axis = name of the y-axis
    mode = a flag to indicate how to labe the axies
    """
    fig, axis = plt.subplots()
    plt.title(title)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)

    #TODO add other modes    
    if ("year" == mode):
        major   = mdates.MonthLocator()  
        major_fmt = mdates.DateFormatter('%b')
        minor = mdates.DayLocator(interval = 5)
    else: 
        major   = mdates.MonthLocator()  
        major_fmt = mdates.DateFormatter('%b')
        minor = mdates.DayLocator()
   
    axis.xaxis.set_major_locator(major)
    axis.xaxis.set_major_formatter(major_fmt)
    axis.xaxis.set_minor_locator(minor)
    fig.autofmt_xdate()


def show_plot():
    """
    prints the plot to a window
    """
    plt.show()  


def line_to_plot(interval, dates, vals):
    """
    generates a line to plot
    interval = the interval to graph
    dates = dates to plot
    vals = values to plot
    returns a modifiable plot
    """
    o_date = []
    o_val = []
    index = 0 
    while (index < len(dates)):
        if (is_in_interval(dates[index], interval)):
            temp = datetime.date(1000, dates[index].month, dates[index].day)
            o_date.append(temp)
            o_val.append(vals[index])
        index += 1
    return plt.plot(o_date, o_val)
