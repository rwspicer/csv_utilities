#!/usr/bin/env python
"""
csv plotter
csv_plot.py
Rawser Spicer
created: 2014/02/03
modified: 2014/12/02

        This utility is designed to plot csv files. It can plot up to 10 
    files at a time, or 1 file with an arbitary number of columns of data

    version 2014.12.2.1:
        undid changes in chec_files, becuase the bug causing the problem was 
    found in csv_lib/csv_args

    version 2014.12.1.1:
        fixed the check_files function, which stoped working at an unknown time
   
    version 2014.7.31.1:
        updated documentation

    version 2014.5.30.1:
        fixed typo in date portion of file header 

    version 2013.3.17.1:
        added support  for the new polot class in csvPlot
    
    version 2014.3.12.1:
        added ArgClass support

    version 2014.2.28.1:
        added support for multiple columns of data

    version 2014.2.12.2:
        fixed up documentation and help

    version 2014.2.12.1:
        added --plot_avg flag, which will plot the a data set over the average 
    of all other data sets

    version 2014.2.10.1:
        the legend will now show the data titile instead of the file name

    version 2014.2.7.2:
        added the legend

    version 2014.2.7.1 (working version 1):
        this is the working version. added a fuction process interval to further
    subdevide the work of csv_plotter function. fixed all documentation

    version 2014.2.6.2:
        added the plotter function to act like a main function in c++

    version 2014.2.6.1:
        polts a csv file with the csv_plot module

    version 2014.2.3.1:
        plots a csv file

"""
import csv_lib.csv_args as csva
from csv_lib.csv_utilities import print_center, check_file, \
                                exit_on_failure, exit_on_success
import csv_lib.csv_plot as csvp
from csv_lib.csv_date import get_last_date
import datetime as dtime 


def get_year(value):
    """
        get a year
        
    arguments    
        value:      (string) the argument from client
    
    returns: 
        a interger year
    """
    if (value == ""):
        return 0
    else:
        return int(value)


def get_interval(value):
    """
        gets an interval from the command line 
    
    arguments:
        value:      (string) the argument from client
    
    returns: 
        an interval string
    """
    if(value == ""):
        return "0000-00-00,0000-00-00"
    else:
        return value


def get_string(value):
    """
        gets a string form clinet or returns "" for no argument
    
    arguments:
        value:      (string)the argument from client
    
    returns: 
        a string
    """
    return value


def get_delta(value):
    """
        turns a number of days input into a datetime.timedelat object
    
    arguments:
        value:  (string) the argument from client
    
    returns: 
        a datetime.timedelat object
    """
    if (value == ""):
        return dtime.timedelta(0)
    else :
        return dtime.timedelta(int(value))


def get_bool(value):
    """
        get boolean from command line
    
    arguments:
        value:   (string)the argument from client
    
    returns:
        a bool 
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
        
    arguments:
        cmds:       ((string)list)the list of command imputs
        file_keys:  ((string)list)the keys that might contain files
    
    returns: 
        a list of valid files
    """
    count = 0  
    files = []
    for key in file_keys:
        try:
            #~ if cmds[key] == "" and key != "--data_0":
                #~ continue
            if not (check_file(cmds[key])):
                print_center("ERROR: invalid data_file, " + cmds[key])
                exit_on_failure()
            else:
                count += 1
                files.append(cmds[key])
        except KeyError:
            if (count == 0) :
                raise KeyError, "no files indicated"
                #print_center("ERROR: no files indicated", '*')
                #print_center("use --data_0 as flag for a singal file")
                #exit_on_failure() 
            else:
                continue

    return files


def process_interval(commands):
    """
        this function processes the commands for making a plot interval
    
    arguments
        commands:   ((string)list) the commands
    
    returns:
        a interval
    """
    year = commands.get_command_value("--year", get_year) 
    interval_string = commands.get_command_value("--time_interval"
														, get_interval)
    days = commands.get_command_value( "--days", get_delta)
    
    if (year != 0):
        return str(year)+"-01-01" , str(year)+"-12-31"
    elif (interval_string != "0000-00-00,0000-00-00"):
        return interval_string.split(',')[0], interval_string.split(',')[1]
    elif (days):
        end = get_last_date(commands['--data_0'])
        return end - days, end
    else:
        return "min", "max"

    #return start, end




UTILITY_TITLE = " plotting utility "
FILES = ("--data_0", "--data_1", "--data_2", "--data_3", "--data_4", 
              "--data_5", "--data_6", "--data_7", "--data_8", "--data_9")
OPT_FLAGS = ("--time_interval", "--output_png", "--title", "--y_label",
               "--x_label", "--year", "--days", "--show", "--plot_avg",
                "--multi_col_mode", "--num_cols") + FILES[1:]
REQ_FLAGS = (FILES[0],)

    
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
    --title: plot title (optional: will be detrimined by the class by default)
    --y_label: y-axis label (optional: will be detrimined by the class by default)
    --x_label: x-axis label (optional: "" by default)
    --show: set to true to show the plot instead of saving it 
            (optional: false by default) 
            WARNING >>> plot will not be witten to screen if unless <<<  
                    >>> back end is changed in csv_plot.py          <<<
    --plot_avg: set to true to plot all data sets over an averge of 
                the other data sets (optional: false by default)
    --multi_col_mode: this flag no longer does any thing as the 
					  PlotClass should work by auto
    --num_cols: this flag no longer does any thing as the 
				PlotClass should work by auto
              """




def csv_plotter():
    """
    this is the csv plotter utility this functon acts like main
    """
    print_center(UTILITY_TITLE, '-')

    try: 
        commands = csva.ArgClass(REQ_FLAGS, OPT_FLAGS, HELP_STRING)
    except RuntimeError, error_message:
        exit_on_failure(error_message[0])
    
    files_to_plot = check_files(commands, FILES)
    start, end = process_interval(commands)
    
   
    plot = csvp.PlotClass(files_to_plot, commands["--output_png"])
 
    plot.set_interval(start, end)
    plot.set_up_plot()
    
    temp = commands.get_command_value("--y_label", get_string)
    if (temp != ""):
        plot.set_y_label(temp)
    temp = commands.get_command_value( "--x_label", get_string)
    if (temp != ""):
        plot.set_x_label(temp)
    temp = commands.get_command_value( "--title", get_string)
    if (temp != ""):
        plot.set_title(temp)
		
    
    if (commands.get_command_value( "--plot_avg", get_bool)):
        plot.plot_avg()
    else:
        plot.plot()
    plot.set_legend()
    
    
    plot.save_plot()   
    
    exit_on_success()


#---run utility----
if __name__ == "__main__":
    csv_plotter()



