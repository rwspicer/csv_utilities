"""
tz_shift.py
time sone shifter
Rawser Spicer
created: 2014/03/05
modified: 2014/03/10

        this utility allows for the conversion between the UTC-0 and UTC-9(AKST) 
    time zones  

    version 2015.1.5.1:
        added example usage

    version 2014.8.8.1:
        updated documentation

    version 2014.3.10.1:
        now uses the csv arg class

"""
from datetime import timedelta
import csv_lib.csv_file as csvf
import csv_lib.csv_args as csva
from csv_lib.csv_utilities import print_center, exit_on_success, exit_on_failure


UTILITY_TITLE = "< Time Zone Shifter >"
HELP_STRING = """
    This utility allows for the conversion between the UTC-0 and UTC-9(AKST)
    time zones in czv files where items in the first column can be read as a
    datetime object
    
    example usage
        python tz_shift.py --in_file=file --out_file=file --timezone=toAK

    --in_file:      the input file <path/filename>
    --out_file:     the output file <path/filename>
    --timezone:     which time zone to change to <"toUTC" | "toAK">
              """
FLAGS = ("--in_file", "--out_file", "--timezone")

    
def interp_tz(value=""):
    """
    gets the time zone to switch to
    
    arguments:
        value:    (string) the value from the command line
    
    retunrs:
        the time zone multiplier
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
    
    try:
        commands = csva.ArgClass(FLAGS, (), HELP_STRING)
    except RuntimeError, (ErrorMessage):
         exit_on_failure(ErrorMessage[0])    

    if commands.is_missing_flags():
        for items in commands.get_missing_flags():
            print_center(" ERROR: flag <" + items + "> is required ", "*")
        exit_on_failure()

    to_utc = commands.get_command_value("--timezone", interp_tz)
    
    try:
        my_file = csvf.CsvFile(commands["--in_file"])
    except IOError:
        print_center("ERROR: input file was not found", '*')
        exit_on_failure()    
        
    header = my_file.get_header()
    dates = my_file.get_dates()
    delta = timedelta(hours = 9*(to_utc))

    if to_utc == 1:
        header[2][0] = "UTC-0"
    elif to_utc == -1:  
        header[2][0] = "UTC-9(AKST)"
    else:
        print_center("toAK or toUTC not specified")
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

