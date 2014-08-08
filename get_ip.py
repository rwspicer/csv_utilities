"""
get_ip.py
Rawser Spicer
created: 2014/02/13
modified: 2014/07/31

    gets the ip adderess from a saved ifconfig output
    
    version 2014.7.31.1:
        updated documentation

    version 2014.5.30.1:
        fixed typo in date portion of file header 

    version 2014.3.12.1:
        now uses ArgClass

    version 2014.2.13.1:
        adds documentation and support for interface


"""
import csv_lib.csv_args as csva
from csv_lib.csv_utilities import print_center, exit_on_success, exit_on_failure



def get_dev(value):
    """
        for fetching the interface from command line. will set to eth0 if no
    value is given
    
    arguments
        value:      (string) the value from command line
    """   
    if (value == ""):
        return "eth0"
    else:
        return value

UTILITY_TITLE = " ip adderess locator "
HELP = """
        this utility can be used to get an ip adderess from the saved output of
    an ifconfig run
    
        --infile:       the input text from ifconfig
        --outfile:      where to write the ip adderss to
        --interface:    the interface for the ip adderess (eth0 by default) 
         """
REQ_FLAGS = ("--infile", "--outfile")
OPT_FLAGS = ("--interface",)



def get_ip():
    """
    gets the ip adderess from a file
    """

    print_center(UTILITY_TITLE, "-")
    try:
        inputs = csva.ArgClass(REQ_FLAGS, OPT_FLAGS, HELP)
    except RuntimeError, error_message:
        exit_on_failure(error_message[0])

    if inputs.is_missing_flags():
        for items in inputs.get_missing_flags():
            print_center(" ERROR: flag <" + items + "> is required ", "*")
        exit_on_failure()    
    
    f_stream = open(inputs['--infile'], 'r')

    while (True):
        line = f_stream.readline()
        line = line.split()
        try:
            if (inputs.get_command_value("--interface", get_dev) == line[0]):
                break
        except IndexError:
            continue
    
    while (True):
        line = f_stream.readline()
        line = line.split()
        seg = line[1].split(':')
    
        if (seg[0] == 'addr'):
            f_stream.close()
            f_stream = open(inputs['--outfile'], 'w')
            f_stream.write(seg[1])
            break
    exit_on_success()    

if __name__ == "__main__":
    get_ip()

