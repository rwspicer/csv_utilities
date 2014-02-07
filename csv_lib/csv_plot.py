"""
CSV Utilitys Plot Module
csv_plot.py
Rawser Spicer
created: 2014/02/05
modified: 2014/02/07

        This module contains the ploting functions for csv_lib library. It
     contains the following functions:
        load_file_to_plot       -- loads a file to plot
        set_up_plot             -- sets up a plots labels
        line_to_plot            -- makes a line to plot
        make_legend_plot        -- makes a legend below the plot
        show_plot               -- shows a plot
        save_plot               -- saves a plot

    version 2014.2.7.2
        added function make_legend_plot

    version 2014.2.7.1
        Updated the set up plot function to work with other modes. Added
    save_plot. Fixed up documentation

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
from csv_lib.csv_utilities import print_center
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
    fig.canvas.set_window_title(title)
  
    if ("year" == mode):
        major   = mdates.MonthLocator()  
        major_fmt = mdates.DateFormatter('%b')
        minor = mdates.DayLocator(interval = 5)
    elif ("month" == mode):
        major   = mdates.MonthLocator()  
        major_fmt = mdates.DateFormatter('%b')
        minor = mdates.DayLocator(interval = 1)
    elif ("day" == mode):
        major   = mdates.DayLocator(interval = 5)  
        major_fmt = mdates.DateFormatter('%b %d')
        minor = mdates.HourLocator(interval = 12)
    else: 
        major   = mdates.MonthLocator()  
        major_fmt = mdates.DateFormatter('%b')
        minor = mdates.DayLocator()

    fig.autofmt_xdate()
    axis.xaxis.set_major_locator(major)
    axis.xaxis.set_major_formatter(major_fmt)
    axis.xaxis.set_minor_locator(minor)


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


def make_legend_plot(plots, names):
    """
    makes a legend for the plot
    plots = the lines being plotted
    names = their names
    """
    plt.legend(plots, names, bbox_to_anchor=(0.5, -0.35), loc='lower center',
                fancybox=True, shadow=True, ncol=2)


def show_plot():
    """
    prints the plot to a window
    """
    plt.show()  


def save_plot(f_name):
    """
    save plot to file of f_name
    f_name = name of the file
    """
    print_center("+++ saving polt to " + f_name + " +++")
    plt.savefig(f_name, bbox_inches='tight')



