"""
relative humidity calulator
rh_calculator.py
Rawser Spicer
created: 2014/01/24
modifyed: 2013/02/10
    

    version 2014.2.10.1
        updated to use new csv_lib name

    update 1: 
        the fill will now olny be apended to starting at the next time 
    step after the final time step in the out put file if the output 
    file alerady exists

   This utility calcualtes relative humidity from air temepeature and dew point 
   data 
"""
import sys
import re
from csv_lib.csv_utilities import read_args, print_center, check_file, \
                          get_command_value, load_file, write_to_csv


def get_cutoff(value):
    """
    gets the cuttoff value from a string
    value = a string of the cutoff value
    returns the value in the value as a float or -5.0 if value is ""
    """
    if (value == ""):
        return -5.0
    else:
        return float(value)
        

def compute_date(date_string):
    """
    converts the date from a string in mm/dd format to a number
    date_string = the date in string form MM/DD
    returns a number in this form MMDD
    """
    month, day = [t(s) for t , s in zip((int, int),
                re.search(r'^(\d+)/(\d+)$',date_string).groups())]
    
    return month*100+day        


def start_date(date):
    """
    gets the start date form a string
    string = a string formated (MM/DD)
    returns the date as a number or 501 the represntation of 05/01 if "" is date
    """
    if (date == ""):
        return compute_date('05/01')
    else: 
        return compute_date(date)
        

def end_date(date):
    """
    gets the end date form a string
    date = a string formated (MM/DD)
    returns the date as a number or 1001 the represntation of 10/01 if "" 
        is date
    """
    if (date == ""):
        return compute_date('10/01')
    else: 
        return compute_date(date)
        
        
def get_month_day(date):
    """
    gets the month and day (MMDD) portion from a YYYYMMDDHHmmSS date number
    date = a date number
    returns MMDD portion of datenumber
    """
    temp = date / 1000000
    temp %= 10000
    return int(temp)
    
    

def precip_check(p_dates, p_vals, at_dates, at_vals, start, end, cutoff):
    """
    this function checks to see if preciptation values lie with in the given 
        date and temperature values. If they do they are written to a new array 
        as is: else bad_val isw written
    p_dates = precip date array
    p_vals = precip value array
    at_dates = air temerature date array
    at_vals = air temerature value array
    start = the start date
    end = the end date
    cutoff = the cutoff temperature
    returns an array of relative humiditys
    """
    bad_val = 6999
    o_val = []
    index = 0
    while (index < len(p_dates)):
        if not(p_dates[index] == at_dates[index]):
            print_center("dates do not match for precipitation and air temp"
                                                                          ,'*')
            sys.exit(1)
            # how to handle this?
        date = get_month_day(p_dates[index])
        if (date < start or date > end):
            o_val.insert(index, bad_val)
        else:
            if (at_vals[index] < cutoff):
                o_val.insert(index, bad_val)
            else:
                o_val.insert(index, p_vals[index])
        index += 1

    return o_val
    

#__________________________START UTILITY
UTILITY_TITLE = "Realative Humidity Calculator"
FLAG_TYPES = ("--precip_infile", "--precip_outfile", "--at_file", 
              "--startdate", "--enddate", "--cutoff")
HELP_STRING = """
        --precip_infile: the path to the precipitation in file
        --pricip_outfile: path to pricipitation out file
        --at_file: the air temp file
        --startdate: the start date (optional)
        --enddate: the end date (optional)
        --cutoff: the cutoff temperature
              """

END_MESSAGE_SUCCESS = "the utility has run successfully"
END_MESSAGE_FAILURE = "the utility was not successfull"

print_center(UTILITY_TITLE, '-')
COMMANDS = read_args(FLAG_TYPES, HELP_STRING)

if not (check_file(COMMANDS["--precip_infile"])):
    print_center("ERROR: invalid precip_infile, " + COMMANDS["--precip_infile"])
    print_center(END_MESSAGE_FAILURE, '-')
    sys.exit(1)
    
if not (check_file(COMMANDS["--at_file"])):
    print_center("ERROR: invalid at_file, " + COMMANDS["--at_file"])
    print_center(END_MESSAGE_FAILURE, '-')
    sys.exit(1)
    
if (check_file(COMMANDS["--precip_outfile"])):
    print_center("file, " + COMMANDS["--precip_outfile"]
                          +", will be appeanded to")
else:
    print_center("file, " + COMMANDS["--precip_outfile"] 
                          + ", not found, it will be created")
  
CUTOFF = get_command_value(COMMANDS, "--cutoff" , get_cutoff)
STARTDATE = get_command_value(COMMANDS, "--startdate" , start_date)
ENDDATE = get_command_value(COMMANDS, "--enddate" , end_date)

try:
    P_IN_DATES, P_IN_VALS, P_IN_HEADER = load_file(COMMANDS["--precip_infile"]
                                                                           , 4)
    AT_DATES, AT_VALS, AT_HEADER = load_file(COMMANDS["--at_file"], 4)
except (BaseException):
    print_center(END_MESSAGE_FAILURE, '-')
    sys.exit(1)
    
P_OUT_VALS = precip_check(P_IN_DATES, P_IN_VALS, AT_DATES, AT_VALS,
                          STARTDATE, ENDDATE, CUTOFF)

try:
    write_to_csv(COMMANDS["--precip_outfile"], P_IN_DATES, P_OUT_VALS
                                                         , P_IN_HEADER)
except (BaseException):
    print_center(END_MESSAGE_FAILURE, '-')
    sys.exit(1)

print_center(END_MESSAGE_SUCCESS, '-')
