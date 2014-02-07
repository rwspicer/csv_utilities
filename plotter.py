#!/usr/bin/env python
"""
csv plotter
csv_plot.py
Rawser Spicer
created: 2014/02/03
modifyed: 2014/02/07

        This utility is designed to plot csv files. It can plot up to 10 
    files at a time. 

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
from csv_lib.csv_utilities import read_args, print_center, check_file, \
                          get_command_value, exit_on_failure, exit_on_success
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
    retuns a list of valid files    
    """
    count = 0  
    files = []
    for key in file_keys:
        try:
            if not (check_file(cmds[key])):
                print_center("ERROR: invalid at_file, " + cmds[key])
                exit_on_failure()
            else:
                count += 1
                files.append(cmds[key])
        except KeyError:
            if (count == 0) :
                print_center("ERROR: no files indicated", '*')
                print_center("use --data_0 as flag for a singal file")
                exit_on_failure() 
            else:
                print_center("+++ file " + key +
                         " not indicated, IGNORING +++") 

    return files


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
    """
    plot_list = []
    for item in files_to_plot:
        dates, values = load_file_to_plot(item)
        temp = line_to_plot(interval, dates, values)
        plot_list.append(temp[0]) 
    return plot_list

def csv_plotter():
    """
    this is the csv plotter utility this functon acts like main
    """
    utility_title = " csv plotter "
    data_files = ("--data_0", "--data_1", "--data_2", "--data_3", "--data_4", 
              "--data_5", "--data_6", "--data_7", "--data_8", "--data_9")
    flag_types = ("--time_interval", "--output_png", "--title", "--y_label",
               "--x_label", "--year", "--days", "--show") + data_files
    help_string = """
    --data_0: the csv file to plot
    --data_[1-9]: other csv fils to plot (optional)
    --output_png: name of the .png file to save the plot to
    --time_interval: the time interval to plot <2000-01-01,2000-12-31>(optional)
    --year: the year to plot (optional)
    --days: days from the last date in the file to plot (optional)
    --title: plot title
    --y_label: y-axis label  
    --x_label: x-axis label
    --show: set to true to show the plot instead of saving it     
              """

    print_center(utility_title, '-')
    commands = read_args(flag_types, help_string)
    
    png = get_command_value(commands, "--output_png", get_file_name)
    
    y_label = get_command_value(commands, "--y_label", get_string)
    x_label = get_command_value(commands, "--x_label", get_string)
    title = get_command_value(commands, "--title", get_string)
    interval, mode = process_interval(commands)    
    
    set_up_plot(title, x_label, y_label, mode)
    
    files_to_plot = check_files(commands, data_files)    
    plots = plot_lines(files_to_plot, interval)
    make_legend_plot(plots, files_to_plot)
    

    if (get_command_value(commands, "--show", get_bool)):
        show_plot()
    else:    
        save_plot(png)
    
    exit_on_success()


#---run utility----
csv_plotter()
