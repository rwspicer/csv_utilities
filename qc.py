#!/usr/bin/env python
"""
qc utility 
qc.py
Rawser Spicer
created: 2014/03/13
modified: 2014/04/14

       this utility preforms quality based on a file with values to compare

    version 2013.4.14.1
        added documetation 
  
"""
from csv_lib.csv_utilities import print_center, exit_on_failure, exit_on_success
import csv_lib.csv_file as csvf
import csv_lib.csv_args as csva
import xlrd
import datetime
import math

def fetch_excel_data(file_name):
    """
    reads excel file data
    file_name : the file to read
    returs a list of two lists [[dates],[values]]
    """
    wb = xlrd.open_workbook(file_name)
    sheet = wb.sheet_by_index(0)
    n_rows = sheet.nrows
    n_cols = sheet.ncols
    o_val = [[],[]]
    for c_index in range(n_cols):
        for r_index in range(n_rows):
            if r_index < 4:
                continue          
            temp = sheet.cell(r_index,c_index)
            if c_index == 0:
                temp.value = datetime.datetime(*xlrd.xldate_as_tuple(temp.value,
                                                                wb.datemode))
            o_val[c_index].append(temp.value)
    return o_val


def is_bv(val):
    """
    checks for a bad value
    val: value to check
    returns true if the value is a bad value
    """
    if math.isnan(val):
        return True
    if val == 6999 or val == 7777 or val == 9999:
        return True
    return False


def qc_func(in_data, xl_data, log_file):
    """
    preforms the quality controll check
    in_data: data to check
    xl_data: data to check with
    log_file: a file to log changes
    retuens fixed data in [[dates],[values]] form
    """    
    f_stream = open(log_file, 'a')    

    for index, items in enumerate(in_data[0]):
        for xidx, xitm in enumerate(xl_data[0]):
            if items == xitm and is_bv(xl_data[1][xidx]):
                f_stream.write(str(items) + ",Manual QC, Orignal:" + \
                                str(in_data[1][index]) + " Replacment: " + \
                                str(xl_data[1][xidx]) + "\n")
                in_data[1][index] = xl_data[1][xidx]
    return in_data[:]

UTILITY_NAME = "< quality control utility >"
REQ_FLAGS = ("--input",)
OPT_FLAGS = ("--insitu", "--short")
HELP_STR = """
            the folowing flags can be used with this utility
            --input: the input (.csv file)
            --short: a correction file (excel format)
            --insitu: a correction file (excel format)

            note: use --short or --insitu, not both 
           """ 

def main():
    print_center(UTILITY_NAME, '-')
    
    try:    
        commands = csva.ArgClass(REQ_FLAGS, OPT_FLAGS, HELP_STR)
    except RuntimeError, (error_message):
        exit_on_failure(error_message[0]) 
    
    if commands.is_missing_flags():
        for items in commands.get_missing_flags():
            print_center(" ERROR: flag <" + items + "> is required ", "*")
        exit_on_failure()    

    try:
        in_file = csvf.CsvFile(commands["--input"], True)
    except IOError:
        print_center("ERROR: a required file was not found", '*')
        exit_on_failure()
    
    try:
        xl_data = fetch_excel_data(commands["--insitu"])
    except KeyError:
        try:
            xl_data = fetch_excel_data(commands["--short"])
        except KeyError:
            print_center("ERROR: an adjustment file has not been provided", "*")
            exit_on_failure()
        except IOError:
            print_center("ERROR: an adjustment file was not found", "*")
            exit_on_failure()
    except IOError:
        print_center("ERROR: an adjustment file was not found", "*")
        exit_on_failure()

    in_data = [in_file[0], in_file[1]]
    
    name = commands["--input"].split('/')[-1].split('.')[0]
    path_str = ""    
    for items in commands["--input"].split('/')[:-2]: 
        path_str += items + '/'
    log_file = path_str + 'qc/' + name + "_qaqc_log.csv"
    
    fixed_data = qc_func(in_data, xl_data, log_file)
    
        
    in_file[0] = fixed_data[0]
    in_file[1] = fixed_data[1]

    in_file.save()

    exit_on_success()




if __name__ == "__main__":
    main()