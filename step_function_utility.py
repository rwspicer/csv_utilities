"""
Step Function Utility
stepFuncUtil.py
Rawser Spicer
created: 2014/01/??
modified: 2014/02/10

    version 2014.2.10.1
        updated to use new csv_lib name
    
    version 2014.02.03.2
        uses the basic csv_utilities lib features

    version 2014.02.03.1
        added support for the csv_utilites module

    update 1: 
        now the unility creates the out put file if it dose not exist and
    appends the data to one that does.

   This utility applys a step function to processed data
to allow for corrections to be applyed to said data
"""

from csv_lib.csv_utilities import read_args, load_file, write_to_csv, \
                                  print_center




def linear_step_function(d_val, l_func):
    """linear step function"""
    o_val = []
    for time_step in d_val:
        val = l_func[1] * time_step + l_func[0]
        o_val.append(val)
    return o_val


def step_function(d_date, d_val, s_date, s_val):
    """
    applys the step function
    d_date = an array of the dates of the input data
    d_val = an array of values from the input data
    s_date = an array of dates from the step file indcating when values need 
    to be modifyed
    s_val = an array of values to modify the input values by 
    returns a corrected array of values
    """
    d_index = len(d_date)-1
    s_index = len(s_date)-1
    o_val = []
    while (d_index >= 0):
        if (d_date[d_index] < s_date[s_index]):
            if (s_index > 0):
                s_index = s_index - 1
                
        if (d_date[d_index] >= s_date[s_index]):
            temp = d_val[d_index] + s_val[s_index]
            o_val.insert(0, temp)
            
        else:
            temp = d_val[d_index]
            o_val.insert(0, temp)
            
        d_index = d_index - 1
        
    return o_val
    
    

UTILITY_TITLE = "Step Function Utility"
FLAGS = ("--infile", "--outfile", "--stepfile")
HELP = """
    To correctly use this python utility:
        $ python track_delay.py --infile=<path>/filename.csv
        --stepfile=<path>/filename.csv --outfile=<path>/filename.csv
                  """
END_MESSAGE_SUCCESS = "the utility has run successfully"
#END_MESSAGE_FAILURE = "the utility was not successfull"

print_center(UTILITY_TITLE, '-')                  

FILE_NAMES = read_args(FLAGS, HELP)
DATA_DATE , DATA_VAL , HEADER = load_file(FILE_NAMES["--infile"], 4)
STEP_DATE , STEP_VAL , S_HEADER = load_file(FILE_NAMES["--stepfile"], 1)
OUT_VAL = step_function(DATA_DATE , DATA_VAL, STEP_DATE, STEP_VAL) 
write_to_csv(FILE_NAMES["--outfile"], DATA_DATE, OUT_VAL, HEADER)

print_center(END_MESSAGE_SUCCESS, '-')

 

