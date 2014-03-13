"""
rad_decoder.py
rawser spicer
created 2014/03/03
modified 2014/03/13
    
    version 2014.2.13.1
        added support for the CsvFile Class
        
    version 2014.3.12.1
        cleanded up a bit 

    this utility extracts the dated from a cdf file

"""
from datetime import datetime
from scipy.io import netcdf
from csv_lib.csv_utilities import exit_on_success, exit_on_failure, print_center
from os import listdir
import os
from os.path import isfile, join
import csv_lib.csv_args as csva
import csv_lib.csv_file as csvf
import sys


def get_list_vars(my_vars):
    """
    makes a list of varibles that are data lists
    my_vars = the set of variables from a cdf file
    """
    lists = []
    for var in my_vars:
        try:
            temp = my_vars[var].getValue()
            #print var + '=' + str(temp)
        except ValueError:
            lists.append(var)
    return lists


def get_times(my_vars):
    """
    get the times from the cdf file( gets every hour)
    my_vars = the variables in the cdf file
    """
    base_time = my_vars['base_time'].getValue()
    times=my_vars['time']
    ts = []
    for time in times:
        temp = datetime.utcfromtimestamp(base_time+time)
        if (temp.minute == 0) :   
            ts.append(temp)
    return ts


def avg_vars(my_vars,lists):
    """
    averges all of the varibles in a list of data 
    my_vars = the list of data
    """
    avg_lists = {}
    for var in lists:
        temp = my_vars[var][:]
        avg = 0   
        rad1avg = [] 
        for index, item in enumerate(temp):
            if index % 60 == 0 and index != 0:
                rad1avg.append(avg/60)    
                avg = 0
            avg+=item
    
        rad1avg.append(avg/60)
        avg_lists[var] = rad1avg

    return avg_lists



UTILITY_TITLE = "radition extractor utility"

FLAGS = ("--in_directory", "--out_directory", "--sitename")
HELP_STR = """
        This utility can be use to extract the data from a directory of 
    .cdf files. it will cread a csv file for ecah data array in the 
    provided cdf files.
        
    flags:
        --in_directory:     the directory containg the input
        --out_directory:    the directory to save the out put
        --sitename:         the name of the site asscosiated with the data          
           """


def main():
    """ the utility """
    print_center(UTILITY_TITLE, '-')
    try:
        commands = csva.ArgClass(FLAGS, (), HELP_STR)
    except RuntimeError, (error_message):
        exit_on_failure(error_message[0]) 

    path = commands["--in_directory"]
    onlyfiles = [f for f in listdir(path) if isfile(join(path,f)) ]

    onlyfiles = [f for f in onlyfiles if (f[-4:] == ".cdf")]

    onlyfiles.sort()

    for f_name in onlyfiles:

        my_file = netcdf.netcdf_file(path+f_name,'r')
    
        my_vars = my_file.variables
  
        times =  get_times(my_vars)
        
        lists = get_list_vars(my_vars)
       
        avgs = avg_vars(my_vars,lists)
        
        
        for index, items in enumerate(avgs):
            
            
            
            f_name = commands["--out_directory"] + items + ".csv"
            out_file = csvf.CsvFile(f_name)
            header = commands["--sitename"] + ',\nTIMESTAMP,' + items \
                                                + '\nUTC+0,UNITS\n,avg\n'
            
            out_file.string_to_header(header)
            out_file.add_dates(times)
            out_file.add_data(1,avgs[items])
         
            out_file.append()
            
           
        my_file.close()

    exit_on_success()

if __name__ == "__main__":
    main()


