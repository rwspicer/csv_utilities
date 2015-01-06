#!/usr/bin/env python
"""
Step Function Utility
stepFuncUtil.py
Rawser Spicer
created: 2014/01/??
modified: 2014/07/31

        This utility applys a step function to processed data
    to allow for corrections to be applyed to said data
    
    version 2015.1.5.1:
        added example usage
    
    version 2014.8.8.1:
        added a class for the utility
    
    version 2014.7.31.1:
        updates documantation.    

    version 2014.3.10.1:
        uses csv_args to handel the command line
    
    version 2014.3.6.1:
        updated to work with the CsvFile class
        the old version apperes to not have been working at all but this one 
        should. it now also has a main finction, and is executible

    version 2014.2.10.1:
        updated to use new csv_lib name
    
    version 2014.02.03.2:
        uses the basic csv_utilities lib features

    version 2014.02.03.1:
        added support for the csv_utilites module

    update 1: 
        now the unility creates the out put file if it dose not exist and
    appends the data to one that does.
  
"""
from csv_lib.csv_utilities import print_center, exit_on_failure, exit_on_success
import csv_lib.csv_file as csvf
import csv_lib.csv_args as csva
import csv_lib.utility as util


UTILITY_TITLE = "Step Function Utility"
FLAGS = ("--infile", "--outfile", "--stepfile")
HELP_STRING = """
        This utility can be used to correct values in a csve file by applying a 
    correction value over time periods specified in an second file
        
    exapmle usage:
        python step_function_utility.py --infile=file --stepfile=file
        --outfile=file
        
        --infile:   <<path>/*.csv>
                the file with the initial values

        --stepfile: <<path>/*.csv>
                the file withe the step values

        --outfile:  <<path>/*.csv>
                file to save output too
                  """

def linear_step_function(d_val, l_func):
    """
    linear step function
        a work in progress    
    """
    o_val = []
    for index, time_step in enumerate(d_val):
        val = l_func[1] * time_step + l_func[0]
        o_val.append(val)
    return o_val


def step_function(d_date, d_val, s_date, s_val):
    """
        Adds the step values to the initila values

    arguments:
        d_date:     ((datetime.dateime)list) an array of the dates of the 
                input data.
        d_val:      ((values)list) an array of values from the input data
        s_date:     ((datetime.dateime)list) an array of dates from the step 
                file indcating when values need to be modifyed
        s_val:      ((values)list) an array of values to modify the input values 
    
    returns:
        a corrected array of values
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


def main():
    """
    main function
    """
    print_center(UTILITY_TITLE, '-')
    
    try:    
        commands = csva.ArgClass(FLAGS, (), HELP_STRING)
    except RuntimeError, (error_message):
        exit_on_failure(error_message[0])   
     
    try:
        my_file = csvf.CsvFile(commands["--infile"], True)
        my_steps = csvf.CsvFile(commands["--stepfile"], True)
    except IOError:
        print_center("ERROR: a required file was not found", '*')
        exit_on_failure()
    my_file[1] = step_function(my_file.get_dates(), my_file[1],
                                    my_steps.get_dates(), my_steps[1])
        
    my_file.save(commands["--outfile"])
    exit_on_success()   

class StepFunctionUtility(util.utility_base):
    """
        this class is the setp function utility class
    """
    def __init__(self, title = UTILITY_TITLE, r_args = FLAGS, o_args = (), 
                       help = HELP_STRING):
        """
            initilizes the utility
        
        arguments:
            title:      (string) the utility title
            r_args:     (list) the required arguments
            o_args:     (list) the optional arguments
            help:       (string) the help
        """
        super(StepFunctionUtility, self).__init__(title , r_args, o_args, help)
       
       
    def step_function(self, d_date, d_val, s_date, s_val):
        """
            the step function
        
        arguments:
            d_date:     ((datetime)list) a list of the data dates
            d_val:      ((float) list) a list of the data values
            s_date:     ((datetime) list) a list of step dates
            s_val:      ((float) list) a list of step values
            
        returns:
            a list of corrected values
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
    
    def main(self):
        """
            main function
        """
        try:
            my_file = csvf.CsvFile(self.commands["--infile"], True)
            my_steps = csvf.CsvFile(self.commands["--stepfile"], True)
        except IOError:
            self.print_center("ERROR: a required file was not found", '*')
            self.exit()
        my_file[1] = self.step_function(my_file.get_dates(), my_file[1],
                                    my_steps.get_dates(), my_steps[1])
        
        my_file.save(self.commands["--outfile"])
    


if __name__ == "__main__":
    util = StepFunctionUtility()
    util.run()
