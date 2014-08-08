"""
CSV Utilitys Plot Module
csv_plot.py
Rawser Spicer
created: 2014/02/05
modified: 2014/08/08

        This module contains the ploting functions for csv_lib library. It
     contains the following functions:
        load_file_to_plot       -- loads a file to plot
        set_up_plot             -- sets up a plots labels
        line_to_plot            -- makes a line to plot
        make_legend_plot        -- makes a legend below the plot
        show_plot               -- shows a plot
        save_plot               -- saves a plot
        
    version 2014.8.8.1:
        updated documentation  
      
    version 2014.3.17.1
        added a class to handle the plotting

    version 2014.2.19.1
        fixed imports

    version 2014.2.12.2
        fixed the axies lables 

    version 2014.2.12.1
        fixed bug where all data for a day was ploted at midnight

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
from matplotlib import use
use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib
#from csv_lib.csv_date import string_to_datetime, is_in_interval
import csv_lib.csv_date as csvd
#from csv_lib.csv_utilities import print_center
import csv_lib.csv_utilities as csvu
import csv_lib.csv_file as csvf



def load_file_to_plot(f_name, skip = 4):
    """
        loads a array of a datetime.datetime object and an array of 
    coorisponding values
    
    arguments
        f_name:     (string)the file name
        skip:       (int) number of rows to skip (defaluts to 4 the data logger
                header length)
    """    
    date_string , value = numpy.loadtxt(f_name, 
                    dtype = {'names':('date' , 'val'),'formats':('S100','f4')},
                    delimiter=',', usecols=(0 , 1), skiprows=skip, unpack=True)
    date = []
    for items in date_string:
        date.append(csvd.string_to_datetime(items))

    date = numpy.array(date)
    return date, value


def set_up_plot(title = "plot", x_axis = "x-axis", y_axis = "y-axis",
                                                    mode = "year"):
    """
        sets up the plot labels
    
    arguments:
        title:      (string) the plots title
        x_axis:     (string) name of the x-axis
        y_axis:     (string) name of the y-axis
        mode:       (string) a flag to indicate how to labe the axies
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
        major   = mdates.DayLocator()  
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


#line_to_plot is a seperate fuction that the class still calls
def line_to_plot(interval, dates, vals, name = "def"):
    """
        generates a line to plot
    
    arguments:
        interval:   (datetime, datetime) the interval to graph
        dates:      ((datetime)list) dates to plot
        vals:       ((float)list) values to plot
    
    returns:
        a modifiable plot
    """
    o_date = []
    o_val = []
    index = 0 
    while (index < len(dates)):
        if (csvd.is_in_interval(dates[index], interval)):
            temp = dates[index]#.replace(1000)
            o_date.append(temp)
            o_val.append(vals[index])
        index += 1

    return plt.plot(o_date, o_val, label = name)    


def make_legend_plot():
    """
        makes a legend for the plot
    """
    #print names
    plt.legend( bbox_to_anchor=(0.5, -0.15), loc='upper center',
                fancybox=True, shadow=True, ncol=2)


def show_plot():
    """
        prints the plot to a window
    """
    plt.show()  


def save_plot(f_name):
    """
        save plot to file of f_name
    
    arguments:
        f_name:     (string) name of the file
    """
    csvu.print_center("+++ saving plot to " + f_name + " +++")
    plt.savefig(f_name, bbox_inches='tight')



class PlotClass:
    """
    a class to create a plot
    """
    def __init__(self, file_names, png = "def.png"):
        """
            this fucntion sets up the plot class
        
        arguments:
            file_names:     ((string)list) list of the filenames
            png:            (string) name of file to save the plot to
        """
        self.plot_files = {}
        for files in file_names:
            try:
                self.plot_files[files] = csvf.CsvFile(files, True)
                temp_key = files
            except IOError:
                exc_str = "' cannot be plotted as it does not exist."
                raise IOError, "The file  '" + files + exc_str 
        self.interval = csvd.make_interval("min","max")
        self.y_label = self.plot_files[temp_key].get_header()[-2][1]
        self.x_label = ""
        self.title = self.plot_files[temp_key].get_header()[0][0]
        self.set_up_plot()
        self.plots = []
        self.save_name = png
        
    def set_interval(self, start, end):
        """
            set the interval for plotting
        
        arguments:
            start:      (string| datetime) the start date
            end:        (string| datetime) the end date
        """
        self.interval = csvd.make_interval(start, end)
    
    def set_y_label(self, label):
        """
            sets the label for the y axixs
            
        arguments:    
            label:      (string)the label
        """
        self.y_label = label
        self.set_up_plot()
        
    def set_x_label(self, label):
        """
            sets the label for the x axis
        
        arguments:    
            label:      (string)the label
        """
        self.x_label = label
        self.set_up_plot()
    
    def set_title(self, label):
        """
            sets the title
        
        arguments:    
            label:      (string)the label
        """
        self.title = label
        self.set_up_plot()
    
    def save_plot(self):
        """
            save plot to file
        """
        plt.axis('tight')
        plt.savefig(self.save_name, bbox_inches='tight' )
        
    def show_plot(self):
        """
            prints the plot to a window
        """
        plt.show()  
        
    def plot(self):
        """
            plot the data points as they are 
        """
        for files in self.plot_files:
            
            temp = self.plot_files[files]
            for items in range(len(temp)):
                if items == 0:
                    continue
                values = csvu.bv_to_nan(temp[items])
                
                label = temp.get_header()[-3][items]
                self.plots.append(line_to_plot(self.interval, temp[0], 
                                                values, label))
                
    def plot_avg(self):
        """
            Plots the the points in a data set as an average over all other
        data sets
        """
        values = []
        titles = []
        dates_set = False 
        for files in self.plot_files:
            temp = self.plot_files[files]
            
            if not dates_set:
                dates = temp[0]

            for cols in range(len(temp)):
                if cols == 0:
                    continue
                titles.append(temp.get_header()[1][cols])
                values.append(csvu.bv_to_nan(temp[cols]))
                
        length = 0
        for items in values:
            if length == 0:
                length = len(items)
            if length != len(items):
                raise RuntimeError, "data sets not same length"
                
        avg = values[0] - values[0]
        num = 0
        
        for items in values:
            avg += items
            num += 1
        avg = avg/num
        index = 0
        for index in range(len(values)):
            self.plots.append(line_to_plot(self.interval, dates,
                                           values[index]/avg, titles[index]))  
            index += 1  
            
            
    def set_legend(self):
        """
            set  up the legend for a plot
        """
        plt.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center',
                fancybox=True, shadow=True, ncol=2)
        
    def set_up_plot(self):
        """
            sets up the plot labels
        """
        fig, axis = plt.subplots()
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        fig.canvas.set_window_title(self.title)

        major_fmt = mdates.DateFormatter('%b %d %Y')
        fig.autofmt_xdate()
        axis.xaxis.set_major_locator(matplotlib.ticker.AutoLocator())
        axis.xaxis.set_major_formatter(major_fmt)
        axis.xaxis.set_minor_locator(matplotlib.ticker.AutoLocator())
