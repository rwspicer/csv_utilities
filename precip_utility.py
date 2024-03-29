"""
preciptation utility
precip_utility.py
Rawser Spicer
created: 2014/01/24
modified: 2015/01/08

         This utility checks to see if the recorded precipitation lies with in
    given paramaters or not.

    version 2015.1.8.1:
        added example usage

    version 2015.1.5.1:
        added example usage

    version 2014.8.8.1:
        updated docs

    version 2014.5.30.1:
        fixed typo in date portion of file header

    version 2014.4.16.1:
        updated header to have the correct utility and file name

    version 2014.3.13.1:
        updated to use datetimes, ArgClass and CsvFile class
    also the older version may not have worked properly, im not sure why it
    wasnt caught but it works now, so use this version or newer

    version 2014.2.10.1:
        updated to use new csv_lib name

    update 1:
        the fill will now olny be apended to starting at the next time
    step after the final time step in the out put file if the output
    file alerady exists


"""
from datetime import datetime
import csv_lib.csv_file as csvf
import csv_lib.csv_args as csva
import csv_lib.csv_date as csvd
from csv_lib.csv_utilities import print_center, exit_on_success, exit_on_failure


def get_cutoff(value):
    """
        gets the cuttoff value from a string

    arguments:
        value:      (string) the cutoff value

    returns
        the value in the value as a float or -5.0 if value is ""
    """
    if (value == ""):
        return -5.0
    else:
        return float(value)


def start_date(date):
    """
        gets the start date form a string

    arguments:
        date:       (string) a string formated (MM/DD)

    returns
        the date as a datetime with year as 1000
    """
    if (date == ""):
        return ( datetime(1004, 5, 1) )
    else:
        return ( datetime(1004, int(date[0:2]), int(date[3:5])) )


def end_date(date):
    """
        gets the end date form a string

    arguments:
        date:       (string) a string formated (MM/DD)

    returns
        the date as a datetime with year as 1000
    """
    if (date == ""):
        return datetime(1004, 10, 1)
    else:
        return datetime(1004, int(date[0:2]), int(date[3:5]))


def precip_check(p_dates, p_vals, at_dates, at_vals, interval, cutoff):
    """
        this function checks to see if preciptation values lie with in the given
    date and temperature values. If they do they are written to a new array
    as is: else bad_val is written

    arguments:
        p_dates:     ((datetime) list)precip date array
        p_vals:      ((float) list)precip value array
        at_dates:    ((datetime) list)air temerature date array
        at_vals:     ((float) list)air temerature value array
        start:       (datetime) the start date
        end:         (datetime) the end date
        cutoff:      (float) the cutoff temperature

    returns
        an array of corrected precip values
    """
    bad_val = 6999
    o_val = []
    index = 0
    while (index < len(p_dates)):
        if not(p_dates[index] == at_dates[index]):
            print_center("dates do not match for precipitation and air temp"
                                                                          ,'*')
            exit_on_failure()
            # how to handle this?
        print (p_dates[index], p_vals[index], at_dates[index], at_vals[index] )
        date = p_dates[index].replace(year = 1004)
        if not(csvd.is_in_interval(date, interval)):
            o_val.insert(index, bad_val)

        elif (at_vals[index] < cutoff):
            o_val.insert(index, bad_val)
        else:
            o_val.insert(index, p_vals[index])
        index += 1

    return o_val


UTILITY_TITLE = "Precipitation Checker"
REQ_FLAGS = ("--precip_infile", "--precip_outfile", "--at_file")
OPT_FLAGS = ("--startdate", "--enddate", "--cutoff")

HELP_STRING = """

        this utility checks preciptation data to see that it lies within
    a given range of dates and temperature. temperatures are written to an
    updated teperature file.

    example usage:
        python precip_utility.py --precip_infile=infile.csv
        --precip_outfile=outfile.csv --at_file=airtemp.csv

        --precip_infile: the path to the precipitation in file
        --pricip_outfile: path to pricipitation out file
        --at_file: the air temp file
        --startdate: the start date (optional)
        --enddate: the end date (optional)
        --cutoff: the cutoff temperature (optional)
              """


def main():
    """ the utility """
    print_center(UTILITY_TITLE, '-')
    try:
        commands = csva.ArgClass(REQ_FLAGS, OPT_FLAGS, HELP_STRING)
    except (RuntimeError, error_message ):
        exit_on_failure(error_message[0])

    if commands.is_missing_flags():
        for items in commands.get_missing_flags():
            print_center(" ERROR: flag <" + items + "> is required ", "*")
        exit_on_failure()

    try:
        at_file = csvf.CsvFile(commands["--at_file"], True)
        p_in_file = csvf.CsvFile(commands["--precip_infile"], True)
    except IOError:
        print_center("ERROR: a required file was not found", '*')
        exit_on_failure()

    cutoff = commands.get_command_value("--cutoff", get_cutoff)
    interval = csvd.make_interval(
                    commands.get_command_value("--startdate" , start_date),
                    commands.get_command_value("--enddate" , end_date))
    print (interval )
    p_in_file[1] = precip_check(p_in_file[0], p_in_file[1], at_file[0],
                                        at_file[1], interval, cutoff)


    if not p_in_file.append(commands["--precip_outfile"]):
        print_center("Old dates indcate no new data to be appended.")
        print_center("No data was written.                         ")

    exit_on_success()


if __name__ == "__main__":
    main()

