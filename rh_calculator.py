"""
relative humidity calulator
rh_calculator.py
Rawser Spicer
created: 2014/01/24
modified: 2014/02/12

    version 2014.5.30.1:
        fixed typo in date portion of file header     

    version 2014.3.12.1:
        now works with csv_lib.csv_file and .csv_args

    version 2014.3.10.1:
        updated to use new csv_lib name

    version 2014.2.3.2:
        uses the basic csv_utilities lib features

    version 2014.2.3.1:
        adds support for the csv_utilities module

    update 1: 
        the fill will now olny be apended to starting at the next time 
    step after the final time step in the out put file if the output 
    file alerady exists

   This utility calcualtes relative humidity from air temepeature and dew point 
   data
"""
import math
import csv_lib.csv_file as csvf
import csv_lib.csv_args as csva
from csv_lib.csv_utilities import print_center, exit_on_success, exit_on_failure


def calc_rh(at_date, at_val, dp_date, dp_val):
    """
    calcualtes the relative humidity
    at_date = air temerature date array
    at_val = air temerature value array
    dp_date = dew point date array 
    dp_val = dew point value array
    returns an array of relative humiditys
    """
    
    comp_val = 6999
    o_val = []
    index = 0
    while (index < len(at_date)):
        rh_val = comp_val
        if not(at_date[index] == dp_date[index]):
            print_center("ERROR: dates do not match for air temp and dew point",
                            "*")
            exit_on_failure()
            # how to handle this?
        if (at_val[index] != comp_val and  dp_val[index] != comp_val):
            denominator = 0.611 * math.exp((17.3 * at_val[index])
                                 / (at_val[index] + 237.3))
            numerator = 0.611 * math.exp((17.3 * dp_val[index]) 
                                / (dp_val[index] + 237.3))
            rh_val = numerator / denominator * 100    
        o_val.insert(index, rh_val)
        index = index + 1
        
    return o_val
    

UTILITY_TITLE = "Realative Humidity Calculator"
FLAGS = ("--at_file", "--dp_file", "--rh_file")
HELP_STR = """
    To correctly use this python utility:
        $ python track_delay.py --at_file=<path>/filename.csv
        --dp_file=<path>/filename.csv --rh_file=<path>/filename.csv
        
                  """

def main():
    """ the utility """
    print_center(UTILITY_TITLE, '-')   
    
    try: 
        commands = csva.ArgClass(FLAGS, (), HELP_STR)
    except RuntimeError, error_message:
        exit_on_failure(error_message[0])

    if commands.is_missing_flags():
        for items in commands.get_missing_flags():
            print_center(" ERROR: flag <" + items + "> is required ", "*")
        exit_on_failure()

    try:
        at_file = csvf.CsvFile(commands["--at_file"], True)
        dp_file = csvf.CsvFile(commands["--dp_file"], True)
    except IOError:
        print_center("ERROR: a required file was not found", '*')
        exit_on_failure()
    
    rh_file = csvf.CsvFile(commands["--rh_file"])
    if not rh_file.exists():
        print_center(rh_file.name() + " not found, it will be created")
        temp = at_file.get_header()
        temp[1][1] = "Relative Humidity\n"
        temp[2][1] = "Percent\n"
        rh_file.set_header(temp)   
    else:
        print_center(rh_file.name() + " found, it will be appended to") 

    rh_data = calc_rh(at_file[0], at_file[1], dp_file[0], dp_file[1])
    rh_file.set_dates(at_file[0])
    rh_file[1] = rh_data

    if not rh_file.append():
        print_center("Old dates indcate no new data to be appended.") 
        print_center("No data was written.                         ")      

    exit_on_success()
 

if __name__ == "__main__":
    main()

    
    

 

