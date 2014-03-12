"""
rad_decoder.py
rawser spicer
created 2014/03/03

    this utility extracts the dated from a cdf file

"""
from datetime import datetime
from scipy.io import netcdf
from csv_lib.csv_utilities import read_args,get_column, exit_on_failure
from os import listdir
import os
from os.path import isfile, join
import csv_lib.csv_args as csva
import csv_lib.csv_file as csvf


def write_to_csv(f_name, dates, vals, header):
    """
    writes to a csv file, creating it with a header if it does not exist
    or appending to it if it does
    f_name = the filename
    dates = the dates coulumn
    vals = the value column
    header = alist of lines to make up the header
    returns nothing
    """
    try:
        if (not os.path.exists(f_name)):
            f_stream = open(f_name, 'w')
            for line in header:
               f_stream.write(line)
            last_date = 0
        else:
            last_date= get_column(f_name, 4, 0, 'datetime')[-1]
            if (last_date >= dates[-1]):
                return
            f_stream = open(f_name, 'a')
    except (ValueError):
        print "error in opening file", f_name, ' for writing\n'
        #sys.exit(1)   
             
    index = 0     
       
    try:
        while (index < len(dates)):
            temp = '%s,%3.2f\n' % (dates[index].isoformat(' '), vals[index])
            f_stream.write(temp)
            index += 1

    except (ValueError):
        print "error in wrting file", f_name, '\n'
        #sys.exit(1)
        
    f_stream.close()


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
HELP_STR = "write me "


def main():
    """ the utility """
    try:
        commands = csva.ArgClass(FLAGS, (), HELP_STR)
    except RuntimeError, (error_message):
        exit_on_failure(error_message[0]) 

    path = commands["--in_directory"]
    onlyfiles = [f for f in listdir(path) if isfile(join(path,f)) ]

    onlyfiles = [f for f in onlyfiles if (f[-4:] == ".cdf")]

    onlyfiles.sort()


    print onlyfiles

    for f_name in onlyfiles:

        my_file = netcdf.netcdf_file(path+f_name,'r')
    
        my_vars = my_file.variables
  
        times =  get_times(my_vars)
        
        lists = get_list_vars(my_vars)
       
        avgs = avg_vars(my_vars,lists)
        

        for items in avgs:
            f_name = commands["--out_directory"] + items + ".csv"
            #out_file = csvf.CsvFile(f_name)
            header = commands["--sitename"] + ',\nTIMESTAMP,' + items \
                                                + '\nUTC+0,UNITS\n,avg\n'
            
            #out_file.string_to_header(header)
            #out_file[0] = (times)
            #out_file[1] = (avgs)
            #out_file.append()
            write_to_csv(f_name, times, avgs[items], header) 
            #print len(avgs[items])
        
           
        my_file.close()


if __name__ == "__main__":
    main()


