#!/usr/bin/env python
"""
csv plotter
csv_plot.py
Rawser Spicer
created: 2014/02/03
modifyed: 2014/03/12

        This utility is designed to plot csv files. It can plot up to 10 
    files at a time, or 1 file with an arbitary number of columns of data

    version 2014.3.12.1
        added ArgClass support

    version 2014.2.28.1
        added support for multiple columns of data

    version 2014.2.12.2
        fixed up documentation and help

    version 2014.2.12.1
        added --plot_avg flag, which will plot the a data set over the average 
    of all other data sets

    version 2014.2.10.1
        the legend will now show the data titile instead of the file name

    version 2014.2.7.2
        added the legend

    version 2014.2.7.1 (working version 1)
        this is the working version. added a fuction process interval to further
    subdevide the work of csv_plotter function. fixed all documentation

    version 2014.2.6.2
        added the plotter function to act like a main function in c++

    version 2014.2.6.1
        polts a csv file with the csv_plot module

    version 2014.2.3.1
        plots a csv file

"""
import csv_lib.csv_args as csva
from csv_lib.csv_utilities import read_args, print_center, check_file, \
                          get_command_value, exit_on_failure, exit_on_success, \
                           get_title, bv_to_nan, load_file_new, get_header
from csv_lib.csv_plot import line_to_plot, show_plot, set_up_plot, \
                             load_file_to_plot, save_plot, make_legend_plot
from csv_lib.csv_date import make_interval, get_last_date
import datetime as dtime 


def get_year(value):
    """
    get a year
    value = the argument from client
    retuns a interger year
    """
    if (value == ""):
        return 0
    else:
        return int(value)


def get_file_name(value):
    """
    get a file name
    value = the argument from client
    retuns a file name
    """
    if (value == ""):
        return "def.png"
    else:
        return value


def get_interval(value):
    """
    gets an interval from the command line 
    value = the argument from client
    retuns an interval string
    """
    if(value == ""):
        return "0000-00-00,0000-00-00"
    else:
        return value


def get_string(value):
    """
    gets a string form clinet or returns "" for no argument
    value = the argument from client
    retuns a string
    """
    return value


def get_delta(value):
    """
    turns a number of days input into a datetime.timedelat object
    value = the argument from client
    retuns a datetime.timedelat object
    """
    if (value == ""):
        return dtime.timedelta(0)
    else :
        return dtime.timedelta(int(value))


def get_bool(value):
    """
    get boolean from command line
    value = the argument from client
    retuns a bool 
    """
    if (value == ""):
        return False
    elif(value == 'T' or value == 't' or value == 'TRUE' or 
                         value == 'True' or value == 'true' ):
        return True
    else:
        return False


def check_files(cmds, file_keys):
    """
    creates a list of files to plot
    cmds = the list of command imputs
    file_keys = the keys that might contain files
    retuns a list of valid files, and the titles of their data  
    """
    count = 0  
    files = []
    titles = []
    for key in file_keys:
        try:
            if not (check_file(cmds[key])):
                print_center("ERROR: invalid at_file, " + cmds[key])
                exit_on_failure()
            else:
                count += 1
                files.append(cmds[key])
                titles.append(get_title(cmds[key]))
        except KeyError:
            if (count == 0) :
                print_center("ERROR: no files indicated", '*')
                print_center("use --data_0 as flag for a singal file")
                exit_on_failure() 
            else:
                print_center("+++ file " + key +
                         " not indicated, IGNORING +++") 

    return files, titles


def process_interval(commands):
    """
    this function processes the commands for making a plot interval
    commands = the commands
    returns a interval
    """
    year = get_command_value(commands, "--year", get_year) 
    interval_string = get_command_value(commands,
                                    "--    time_interval", get_interval)
    days = get_command_value(commands, "--days", get_delta)
    
    if (year != 0):
        interval = make_interval(str(year)+"-01-01", str(year)+"-12-31")
        mode = "year"
    elif (interval_string != "0000-00-00,0000-00-00"):
        interval = make_interval(interval_string.split()[0],
                                 interval_string.split()[2])
        mode = "month"
    elif (days):
        end = get_last_date(commands['--data_0'])
        interval = make_interval(end - days, end)
        mode = "day"
    else:
        interval = make_interval("min", "max")
        mode = "year"

    return interval, mode


def plot_lines(files_to_plot, interval):
    """
    plots lines
    files_to_plot: the data files to plot
    interval: the inteval over which to plot them
    """
    plot_list = []
    for item in files_to_plot:
        dates, values = load_file_to_plot(item)
        values = bv_to_nan(values)
        temp = line_to_plot(interval, dates, values)
        plot_list.append(temp[0]) 
    return plot_list


def plot_lines_mcm(data_to_plot, interval, num_cols):
    """
    plots lines
    **** this version works for files with mulitple columns
    data_to_plot: the data files to plot
    interval: the inteval over which to plot them
    num_cols: the number of columns
    """
    plot_list = []
    dates = data_to_plot[0]
    index = 1 # start at 1 b/c dates are at 0
    while (index < num_cols):
        values = data_to_plot[index]
        values = bv_to_nan(values)
        temp = line_to_plot(interval, dates, values)
        plot_list.append(temp[0]) 
        index += 1
    return plot_list


def plot_lines_as_avg(files_to_plot, interval):
    """
    plots each lines over the average of the other lines
    files_to_plot: the data files to plot
    interval: the inteval over which to plot them
    """
    plot_list = []
    for index_o, item_o in enumerate(files_to_plot):
        dates, values = load_file_to_plot(item_o)
        values = bv_to_nan(values)
        num = 0
        avg_total = values - values
        for index_i, item_i in enumerate(files_to_plot):
            if not(index_i == index_o):
                try:
                    avg_total += bv_to_nan(load_file_to_plot(item_i)[1])
                    num += 1
                except ValueError:
                    print_center(" ERROR: in plot_lines_as_avg      ", "*")
                    print_center(" ERROR: data sets not same length ", "*")
                    exit_on_failure()
        if (num):        
            avg = avg_total / num
        else:
            print_center(">>> WARNING: in plot_lines_as_avg         <<<")
            print_center(">>>          no data for average ploting  <<<")
            print_center(">>>          plottting values over 1      <<<")
            avg = 1        
        plot_val = values / avg    
        
        temp = line_to_plot(interval, dates, plot_val)
        plot_list.append(temp[0]) 
    return plot_list


def plot_lines_as_avg_mcm(data_to_plot, interval):
    """
    plots each lines over the average of the other lines
    **** this version works for files with mulitple columns
    data_to_plot: the data files to plot
    interval: the inteval over which to plot them
    """
    plot_list = []
    for index_o, item_o in enumerate(data_to_plot):
        if (index_o==0):        
            dates = item_o
            continue
         
        values = bv_to_nan(item_o)
        num = 0
        avg_total = values - values
        for index_i, item_i in enumerate(data_to_plot):
            if index_i == 0:
                continue
            if not(index_i == index_o):
                try:
                    avg_total += bv_to_nan(item_i)
                    num += 1
                except ValueError:
                    print_center(" ERROR: in plot_lines_as_avg      ", "*")
                    print_center(" ERROR: data sets not same length ", "*")
                    exit_on_failure()
        if (num):        
            avg = avg_total / num
        else:
            print_center(">>> WARNING: in plot_lines_as_avg         <<<")
            print_center(">>>          no data for average ploting  <<<")
            print_center(">>>          plottting values over 1      <<<")
            avg = 1        
        plot_val = values / avg    
        
        temp = line_to_plot(interval, dates, plot_val)
        plot_list.append(temp[0]) 
    return plot_list



UTILITY_TITLE = " plotting utility "
FILES = ("--data_0", "--data_1", "--data_2", "--data_3", "--data_4", 
              "--data_5", "--data_6", "--data_7", "--data_8", "--data_9")
FLAGS = ("--time_interval", "--output_png", "--title", "--y_label",
               "--x_label", "--year", "--days", "--show", "--plot_avg",
                "--multi_col_mode", "--num_cols") + FILES
    
HELP_STRING = """
    --data_0: the csv file to plot
    --data_[1-9]: other csv fils to plot (optional)
    --output_png: name of the .png file to save the plot to
    --time_interval: the time interval to plot <2000-01-01,2000-12-31>(optional)
    --year: the year to plot (optional)
    --days: days from the last date in the file to plot (optional)
                    +++ NOTICE: if one of the above time interval  +++ 
                    +++ options in not  selected the entire data   +++
                    +++ sets will be plotted                       +++
    --title: plot title (optional: "" by default)
    --y_label: y-axis label (optional: "" by default)
    --x_label: x-axis label (optional: "" by default)
    --show: set to true to show the plot instead of saving it 
            (optional: false by default) 
            WARNING >>> plot will not be witten to screen if unless <<<  
                    >>> back end is changed in csv_plot.py          <<<
    --plot_avg: set to true to plot all data sets over an averge of 
                the other data sets (optional: false by default)
    --multi_col_mode: the first file has multiple columns of data 
                      (optional: false by default)
    --num_cols: the number columns that have data, the date column should 
                alaways be column 0 and should NOT! be included in this number 
              """




def csv_plotter():
    """
    this is the csv plotter utility this functon acts like main
    """
    print_center(UTILITY_TITLE, '-')

    try: 
        commands = csva.ArgClass((), FLAGS, HELP_STRING)
    except RuntimeError, error_message:
        exit_on_failure(error_message[0])
    
    png = commands.get_command_value( "--output_png", get_file_name)
    
    y_label = commands.get_command_value("--y_label", get_string)
    x_label = commands.get_command_value( "--x_label", get_string)
    title = commands.get_command_value( "--title", get_string)
    interval, mode = process_interval(commands)    
    
    set_up_plot(title, x_label, y_label, mode)
    
    data_to_plot, titles = check_files(commands, FILES) 
    
    if (commands.get_command_value( "--multi_col_mode", get_bool)):

        num_cols = commands.get_command_value("--num_cols", get_year) 
        num_cols += 1  
        
        titles = get_header(data_to_plot[0], 4)[3:(3+num_cols)]    
        data_to_plot = load_file_new(data_to_plot[0], 4, num_cols)     
        
    
        if (commands.get_command_value( "--plot_avg", get_bool)):
            plots = plot_lines_as_avg_mcm(data_to_plot, interval)
        else:
            plots = plot_lines_mcm(data_to_plot, interval, num_cols)        

    else:
      
        if (commands.get_command_value( "--plot_avg", get_bool)):
            plots = plot_lines_as_avg(data_to_plot, interval)
        else:
            plots = plot_lines(data_to_plot, interval)

    make_legend_plot(plots, titles)


    if (commands.get_command_value( "--show", get_bool)):
        show_plot()
    else:    
        save_plot(png)
    
    exit_on_success()


#---run utility----
if __name__ == "__main__":
    csv_plotter()



