"""
relative humidity calulator
rh_calculator.py
Rawser Spicer
created: 2014/01/24
modifyed: 2014/02/10

    version 2014.2.10.1
        updated to use new csv_lib name

    version 2014.02.03.2
        uses the basic csv_utilities lib features

    version 2014.02.03.1:
        adds support for the csv_utilities module

    update 1: 
        the fill will now olny be apended to starting at the next time 
    step after the final time step in the out put file if the output 
    file alerady exists

   This utility calcualtes relative humidity from air temepeature and dew point 
   data
"""

import sys
import math
from csv_lib.csv_utilities import read_args, load_file, write_to_csv, \
                                    print_center


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
            print "dates do not match for air temp and dew point"
            sys.exit(1)
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
    

#________________________________start utility
UTILITY_TITLE = "Realative Humidity Calculator"
FLAGS = ("--at_file", "--dp_file", "--rh_file")
HELP_STR = """
    To correctly use this python utility:
        $ python track_delay.py --at_file=<path>/filename.csv
        --dp_file=<path>/filename.csv --rh_file=<path>/filename.csv
        
                  """

END_MESSAGE_SUCCESS = "the utility has run successfully"
#END_MESSAGE_FAILURE = "the utility was not successfull"
                  
print_center(UTILITY_TITLE, '-')
FILE_NAMES = read_args(FLAGS, HELP_STR)
AT_DATE , AT_VAL , AT_HEADER = load_file(FILE_NAMES["--at_file"], 4)

#temp header fix up
TEMP = AT_HEADER[1].split(',')
TEMP[1] = "Relative Humidity"
AT_HEADER[1] = TEMP[0] + ',' + TEMP[1] + '\n'

TEMP = AT_HEADER[2].split(',')
TEMP[1] = "Percent"
AT_HEADER[2] = TEMP[0] + ',' + TEMP[1] + '\n'

DP_DATE , DP_VAL , DP_HEADER = load_file(FILE_NAMES["--dp_file"], 4)
RH_VAL = calc_rh(AT_DATE , AT_VAL, DP_DATE, DP_VAL) 

write_to_csv(FILE_NAMES["--rh_file"], AT_DATE, RH_VAL, AT_HEADER)

print_center(END_MESSAGE_SUCCESS, '-')

 

