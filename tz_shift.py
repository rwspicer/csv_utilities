"""
tz_shift.py
time sone shifter
Rawser Spicer
created: 2014/03/05
modifyed: 2014/03/05

    this utility allows for the conversion between the UTC-0 and UTC-9(AKST) 
    time zones  

"""
from datetime import timedelta
import csv_lib.csv_file as csvf
from csv_lib.csv_utilities import read_args, get_command_value, print_center, \
                                  exit_on_success, exit_on_failure


UTILITY_TITLE = "< Time Zone Shifter >"
HELP_STRING = """
    This utility allows for the conversion between the UTC-0 and UTC-9(AKST)
    time zones in czv files where items in the first column can be read as a
    datetime object

    --in_file:      the input file <path/filename>
    --out_file:     the output file <path/filename>
    --timezone:     which time zone to change to <"toUTC" | "toAK">
              """
FLAGS = ("--in_file", "--out_file", "--timezone")


def check_flags(cmds, req_flags):
    """
    checks to see that all required flags are filled out
    if a flag is missing it is printed and the program exits
    
    cmds: the commands from command line
    req_flags: list of requitred flags    
    """
    missing = []
    for item in req_flags:
        try:
            cmds[item]
        except KeyError:
            missing.append(item)
    if len(missing) != 0:
        for item in missing:       
            print_center(" ERROR: <" + item + "> must be defined ", "*")
        exit_on_failure()

    
def interp_tz(value=""):
    """
    gets the time zone to switch to
    value - the value from the command line
    """
    if (value == "toAK"):
        return -1
    elif (value == "toUTC"):
        return 1
    else:
        return 0


def main():
    """ main function """
    print_center(UTILITY_TITLE, "-")
    commands = read_args(FLAGS, HELP_STRING)
    to_utc = get_command_value(commands, "--timezone", interp_tz)
    check_flags(commands, FLAGS)
    
    my_file = csvf.CsvFile(commands["--in_file"])
    header = my_file.get_header()
    dates = my_file.get_dates()
    delta = timedelta(hours = 9*(to_utc))

    if to_utc == 1:
        header[2][0] = "UTC-0"
    elif to_utc == -1:  
        header[2][0] = "UTC-9(AKST)"
    else:
        print "toAK of toUTC not specifyed"
    print_center("Time Zone will be " + header[2][0])

    newtimes = []
    for times in dates:
        newtimes.append(times + delta)

    my_file.set_header(header)
    my_file.set_dates(newtimes)
    my_file.save(commands["--out_file"])
    exit_on_success()

if __name__ == "__main__":
    main()

