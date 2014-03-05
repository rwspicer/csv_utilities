"""
CSV Utilities 
csv_utilities.py
Rawser Spicer
created: 2014/01/31
modified: 2014/02/19

    TODO:
        --update execption types
        --update to datetime
        --load_file_new need work
        --update load_file to load_file_new

        This module contains the basic utilities for csv_lib library. It
    contains the following functions:
        read_args                   -- reads command line arguments
        get_command_value           -- gets the value form a command line 
                                       argument
        date_to_num                 -- converts a date string to a number
        num_to_date                 -- converts a number to a date string
        get_last_date_in_file       -- gets the last date in a file as a number
        check_file                  -- checks if a file exists
        get_header                  -- makes a list of the cells in the header 
                                       of the file
        get_title                   -- gets the title of a files data 
        get_column                  -- loads a colund
        load_file_new               -- eventual replacment for load file       
        load_file                   -- load a file
        write_to_csv                -- writes to a csv file
        write_rep                   -- writs a charicter n times
        print_center                -- prints a string in the center of a 
                                       console
        exit_on_failure             -- exit function for failure
        exit_on_success             -- exit function for success
        bv_to_nan                   -- function to relpace bad values in an 
                                       array with nan

    
    version 2014.2.28.1:
        load_file_new no longer has unpack feature and it loads a file starting 
        at column 0 to the size provided
          
    version 2014.2.19.1:
        added get_column and load_file_new
   
    version 2014.2.17.1:
        added bv_to_nan 

   version 2014.2.10.1:
        added get_header, and get_title functions

    version 2014.2.7.1:
        added exit_on_success, updated documentation 

    version 2014.2.6.1:
        changed some of the basic execptions
        added exit on failure

    version 2014.2.3.1:
        reorginized file and finished all commnets

    version 2014.1.31 :
        This is the initial version of this csv file utility package. It was 
        desgined to work with csv files that have a singal date column and a 
        singial value column. It includes :
            -- date_to_num & num_to_date: 
                functions for converting between between '"YYYY-MM-DD hh:mm:ss"'
                date strings and YYYYMMDDhhmmss date numbers
            -- load_file: 
                a function for loading csv files
            -- get_last_date_in_file:
                gets the last date in a file
            -- write_to_csv:
                 writes to a csv file
           -- check_file:
                checks if a file exists
           -- write_rep & print center:
                functions to help visulaize the progress of a utility
           -- read_args:
                reads argumnts from the command line
           -- get_command_value:
                gets the value from an given command
 
                                      
    
"""
import os
import sys
import numpy
import re
import csv_date as csvd


def read_args(valid_flags, string):
    """
    reads argumens from the command line based on provided flags
    """
    cmd = []
    for index in sys.argv:
        cmd = cmd + index.split("=")
    cmd.pop(0)
    ret_val = {}

    for index , item in enumerate(cmd):
        if (index % 2 == 0):
            found = False
            
            for flags in valid_flags:
                if (item == flags):
                    found = True
                    ret_val[flags] = cmd[index+1] 
                
                elif ('--help' == item):
                    found = True
                    print string
                    exit_on_failure(" help requested exiting ")
                    
            if not found:
                print_center(" ERROR: flag unknown " + item +' ', '*')
                print_center("use <--help> for information on " + \
                                "correct use of this utility")
                print_center('*','*')
                exit_on_failure()
                
    return ret_val



def get_command_value(cmds, key, func):
    """
    gets a value entered at the command line based on a function that the cilent 
    has passed as input
    cmds = the array of commands
    key = the key to access
    func = a function that takes one argument at returns a value 
    """
    try:
        value = cmds[key]
    except KeyError:
        value = ""
    return func(value)
    
   
   
def date_to_num(con_val):
    """ 
    converts a date to a number
    con_val = a string of format '"yyyy-mm-dd hh:MM:ss"' to be converted to a 
    number that looks like this yyyymmddhhMMss
        example '"2013-01-10 10:00:00"' => 20130110100000
    returns a number in yyyymmddhhMMss format
    """
    ts_numbers = [t(s) for t , s in zip((int, int, int, int, int, int),
        re.search(r'^"(\d+)-(\d+)-(\d+) (\d+):(\d+):(\d+)"$',con_val).groups())]
        
    return 100*(ts_numbers[5]+10*(ts_numbers[4]+10*(ts_numbers[3]
                +100*(ts_numbers[2]+100*(ts_numbers[1]+100*(ts_numbers[0]))))))
                
                
                
def num_to_date(con_val):
    """
    converts a number back to a date string
    con_val = a number of format yyyymmddhhMMss to be converted to a string in
    '"yyyy-mm-dd hh:MM:ss"' format
        example  20130110100000 => '"2013-01-10 10:00:00"'
    returns date/time string in  '"2013-01-10 10:00:00"' format
    """
    con_val /= 100
    sec = int(con_val % 10)
    
    con_val /= 10
    minute = int(con_val % 10)
    
    con_val /= 10
    hour = int(con_val % 100)
    
    con_val /= 100
    day = int(con_val % 100)
    
    con_val /= 100
    month = int(con_val % 100)
    
    con_val /= 100
    year = int(con_val % 100000)
    
    date = '"%04d-%02d-%02d %02d:%02d:%02d"' % (year, month, day, hour,
        minute, sec )
        
    return date
    
    
def check_file(f_name):
    """
    checks if a file exsts
    f_name = name of the file 
    """
    if not (os.path.exists(f_name)):
        #print_center("File, " + f_name + ", not found")
        return False
    else:
        return True
   
    
def get_last_date_in_file(f_name):
    """
    gets the last date in a czv file
    f_name = the name of the file
    returns the last date in the file
    """
    try:
        dates = load_file(f_name, 4)[0]
    except (BaseException):
        print "unable to get last date from file", f_name, '\n'
        #sys.exit(1)   
    return dates[-1]  
    

def get_header(f_name, h_len):
    """
    gets the header from the file as a list
    f_name = the filename
    h_len = the length of the header
    """
    h_list = []
    try:
        f_stream = open(f_name, 'r')
    except IOError:
        print_center("ERROR: Reading Header", '*')
        exit_on_failure()
    
    index = 0 
    while (index < h_len):
        #h_list += f_stream.readline().replace('\n','').split(',') 
        h_list += f_stream.readline().split(',') 
        index += 1  
    return h_list


def get_title(f_name, h_len = 4, title_cell = 3):
    """
    get the files title
    f_name = the filename
    h_len = the length of the header
    title_cell = the cell containg the title
    """
    return get_header(f_name, h_len)[title_cell]


def get_column(f_name, h_len, col, d_type):
    """
    gets a column of data from a file
    f_name = the file
    h_len = header length
    col = column to read
    d_type= datatype
    """
    f_value = numpy.loadtxt(f_name, delimiter=',', usecols=(col ,),
            skiprows=h_len, 
            dtype = '|S100')
    r_value = []

    for items in f_value:
        if d_type == 'float':
            temp = float(items)
        elif d_type == 'datetime':
            temp = csvd.string_to_datetime(items)
        else:
            temp = items
        r_value.append(temp)

    r_value = numpy.array(r_value)        
    return r_value


def load_file_new(f_name, h_len, cols):#, unpack = True):
    """
    new load file finction, allows arbitrary number of columns to be loaded from'
    a csv file. if the colum 0 is given as on of the columns it will evalute to 
    datetime.dattime objects; otherwise it will evaulate as a float.
    f_name = the file name
    h_len = length of the header
    cols = # of columns in file
    """
    r_list = []
    items = 0
    while (items < cols):
        if items == 0:
            d_type = "datetime"
        else:
            d_type = "float"
        r_list.append(get_column(f_name, h_len, items, d_type))
        items += 1    
    return numpy.array(r_list)
    # --------- unpack feature ------- perhapse work out later
    #if unpack:
    #    if len(cols) >1:
    #        return [r_list[field] for field in cols ]
    #    else:
    #        return r_list[cols[0]]
    # else:
    #    #temp = []
    #    #for items in r_list.keys():
    #    #    temp.append
    #    #r_list = temp 
    #    return r_list

def load_file(f_name, rows_to_skip):
    """
    loads a csv file to two arrays and the lines indicated as a header
    into a list
    f_name = the file to read
    rows_to_skip = indicates the number of rows that are the header 
    returns an array of dates in # form, an array of values corrisponding with 
    said dates, and a list of the lines in the header.
    """
    try:
        f_stream = open(f_name, 'r')
        header = []
        index = 0
        while (index < rows_to_skip):
            header.append(f_stream.readline())
            index += 1
        f_stream.close()
    except (BaseException): 
        print_center('error loading file header stage, ' + f_name, '*') 
        #sys.exit(1)    
            
    try:
        date , value = numpy.loadtxt(f_name, delimiter=',', usecols=(0 , 1),
           converters={0: date_to_num}, skiprows=rows_to_skip, unpack=True)
    except (BaseException):
        print_center('error loading file data stage, ' + f_name, '*') 
        sys.exit(1)
        
    return date , value, header
     
    
    
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
            last_date = get_last_date_in_file(f_name)
            f_stream = open(f_name, 'a')
    except (BaseException):
        print "error in opening file", f_name, ' for writing\n'
        #sys.exit(1)   
           
    if (dates[-1] == last_date):
        print_center("no new dates to write file " + f_name + \
                        " will not be changed")
        f_stream.close()
        return
             
    index = 0
    if (last_date !=0):
        while (dates[index] <= last_date):
            index += 1        
            
    try:
        while (index < len(dates)):
            temp = '%s,%3.2f\n' % (num_to_date(dates[index]), vals[index])
            f_stream.write(temp)
            index += 1

    except (BaseException):
        print "error in wrting file", f_name, '\n'
        sys.exit(1)
        
    f_stream.close()

        
        
def write_rep(length, fill = ' '):
    """
    writs the fill char to a string length times
    length = the number of times to write
    fill = the charicter to write
    """
    string = ""
    index = 0
    while (index < length):
        string += fill
        index += 1
    return string
    


def print_center(string, fill=' ', size=80):
    """
    prints strings in the center of a terminal window
    string = the string to be written
    fill = the fill char
    size = size of terminal window 
    """
    str_len = len(string)
    space = (size - str_len) / 2
    if (str_len % 2 == 0):
        print write_rep(space, fill) + string + write_rep(space, fill)
    else:    
        print write_rep(space + 1 , fill) + string + write_rep(space, fill)
        


def exit_on_failure(msg = " the utility was not successfull "):
    """
    displays an message and then termiates a utility
    msg = the message displayed
    """
    print_center(msg,'-') 
    sys.exit(1)
    
    
def exit_on_success(msg = "the utility has run successfully"):
    """
    prints the exit on sucess message
    msg = the message to be displayed
    """
    print_center(msg,'-')
    sys.exit(0)


def bv_to_nan(array):
    """
    replaces the bad values, 6999, 7777, 9999 with nan values
    array = the array to find bad values in
    array is returned
    """
    index = 0
    while (index < len(array)):
        if (6999 == array[index] or 7777 == array[index] 
                                 or 9999 == array[index]):
            print array[index]
            array[index] = numpy.nan
        index += 1
    return array



 
    
