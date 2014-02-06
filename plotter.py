#!/usr/bin/env python
"""
csv plotter
csv_plot.py
Rawser Spicer
2014/02/03

version 2014.2.6.2
    added the plotter function to act like a main function in c++

version 2014.2.6.1
    polts a csv file with the csv_plot module

version 2014.2.3.1
    plots a csv file

"""

from csv_lib.csv_utilities import read_args, print_center, check_file, \
                          get_command_value, exit_on_failure
from csv_lib.csv_plot import *

def get_year(value):
    if (value == ""):
        return 0
    else:
        return int(value)

def get_file_name(value):
    if (value == ""):
        return "DEFAULT_SAVE_NAME"
    else:
        return value

def get_interval(value):
    if(value == ""):
        return "0000-00-00,0000-00-00"
    else:
        return value

def get_string(value):
    return value

def get_int(value):
    if (value == ""):
        return 0     
    return int(value)

# move to csv_utilities.py?
def check_files(cmds,file_keys):
    count = 0    
    for key in file_keys:
        try:
            if not (check_file(cmds[key])):
                print_center("ERROR: invalid at_file, " + cmds[key])
                exit_on_failure()
            else:
                count += 1
        except KeyError:
            if (count == 0) :
                print_center("ERROR: no files indicated", '*')
                print_center("use --data_0 as flag for a singal file")
                exit_on_failure() 
            else:
                print_center("+++ file " + key +
                         " not indicated, IGNORING +++") 
    return count



def csv_plotter():
    """
    this is the csv plotter utility this functon acts like main
    """
    utility_title = " csv plotter "
    data_files = ("--data_0", "--data_1", "--data_2", "--data_3", "--data_4", 
              "--data_5", "--data_6", "--data_7", "--data_8", "--data_9")
    flag_types = ("--time_interval", "--output_png", "--title", "--y_label",
               "--x_label", "--year", "--days") + data_files
    help_string = """
      --data_0: the csv file to plot
      --data_[1-9]: other csv fils to plot (optional)
      --time_interval: the time interval to plot
      --output_png: name of the .png file to save the plot to
              """
    print flag_types
    end_message_success = "the utility has run successfully"



    print_center(utility_title, '-')
    commands = read_args(flag_types, help_string)

    count = check_files(commands,data_files)


    year = get_command_value(commands, "--year", get_year) 
    interval_string = get_command_value(commands,
                                    "--    time_interval",get_interval)
    days = get_command_value(commands,"--days", get_int)
    png = get_command_value(commands, "--output_png", get_file_name)
    
    if (year != 0):
        interval = make_interval(str(year)+"-01-01", str(year)+"-12-31")
    elif (interval_string != "0000-00-00,0000-00-00"):
        interval = make_interval(interval_string.split()[0],
        interval_string.split()[2])
    elif (days < 0):
        interval = make_interval("min","max")
        #todo
        #get last date in file
        #make_interval(lastdate - days, lastdate)
    else:
        interval = make_interval("min","max")
    
    
    dates,values = load_file_to_plot(commands['--data_0'])
    dates_1,values_1 = load_file_to_plot(commands['--data_1'])
    dates_2,values_2 = load_file_to_plot(commands['--data_2'])
    
    y_label = get_command_value(commands, "--y_label", get_string)
    x_label = get_command_value(commands, "--x_label", get_string)
    title = get_command_value(commands, "--title", get_string)
    """
    y_label = "degerees celsius"
    x_label = "months of " + str(interval)
    title = "barrow daily average temps 2001"
    """
    set_up_plot(title, x_label, y_label)
    
    line_to_plot(interval,dates,values)
    line_to_plot(interval,dates_1,values_1)
    line_to_plot(interval,dates_2,values_2)
    
    show_plot()
    
    
    print_center(end_message_success, '-')



#---run utility----
csv_plotter()
