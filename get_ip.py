"""
get_ip.py
Rawser Spicer
created: 2014/02/13
modifyed: 2014/02/14

    gets the ip adderess from a saved ifconfig output

    version 2014.2.13
        adds documentation and support for interface


"""
from csv_lib.csv_utilities import read_args, get_command_value, print_center,\
                                    exit_on_success



def get_dev(value):
    """
    for fetching the interface from command line. will set to eth0 if no
    value is given
    value: the value from command line
    """   
    if (value == ""):
        return "eth0"
    else:
        return value


def get_ip():
    """
    gets the ip adderess from a file
    """
    help = """
        this utility can be used to get an ip adderess from the saved output of
    an ifconfig run
    
        --infile:       the input text from ifconfig
        --outfile:      where to write the ip adderss to
        --interface:    the interface for the ip adderess (eth0 by default) 
           """
    print_center(" ip adderess locator ", "-")

    inputs = read_args(("--infile", "--outfile", "--interface"), help )


    f_stream = open(inputs['--infile'], 'r')

    while (True):
        line = f_stream.readline()
        line = line.split()
        try:
            if (get_command_value(inputs, "--interface", get_dev) == line[0]):
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

get_ip()

