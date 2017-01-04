"""
relative humidity calulator
rh_calculator.py
Rawser Spicer
created: 2014/01/24
modified: 2015/09/01

    version 2015.9.1.1:
        removed some extra spaces

    version 2015.1.8.1:
        updated help

    version 2014.8.14.1:
        now uses the utility class

    version 2014.8.8.1
        upadated docs

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
#import csv_lib.csv_args as csva
#from csv_lib.csv_utilities import print_center, exit_on_success, exit_on_failure
import csv_lib.utility as util


def calc_rh(at_date, at_val, dp_date, dp_val):
    """
        calcualtes the relative humidity
    arguments:
        at_date:    ((datetime) list) air temerature date array
        at_val:     ((float) list) air temerature value array
        dp_date:    ((datetime) list) dew point date array
        dp_val:     ((float) list) dew point value array
    returns:
        an array of relative humiditys
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
        this utility takes air tempture and dew point data as input and
    calculates the relative humidity for each time step

    flags:
        --at_file:      <file> the input air tempeature csv file
        --dp_file:      <file> the input dewpoint csv file
        --rh_file:      <file> the out put relative humidity file

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



class rh_util(util.utility_base):
    """
        this class is used as a relative humiditiy calculator.
    """

    def __init__(self):
        """
            sets up utility
        """
        super(rh_util, self).__init__("Realative Humidity Calculator" ,
                    ("--at_file", "--dp_file", "--rh_file") ,(), "help")

        self.help =  """
        To correctly use this python utility:
        $ python track_delay.py --at_file=<path>/filename.csv
        --dp_file=<path>/filename.csv --rh_file=<path>/filename.csv

        """

    def load_files(self):
        """
            loads the files form the names in the arguments
        """
        try:
            self.at_file = csvf.CsvFile(self.commands["--at_file"], True)
            err = "--at_file"
            self.dp_file = csvf.CsvFile(self.commands["--dp_file"], True)
            err = "--dp_file"
            self.rh_file = csvf.CsvFile(self.commands["--rh_file"])
            err = "--rh_file"
        except IOError:
            self.errors.set_error_state("File Not Found",
                            "A required file was not found",
                            err)
        if not self.rh_file.exists():
            self.print_center(self.rh_file.name() + \
                                        " not found, it will be created")
            temp = self.at_file.get_header()
            temp[1][1] = "Relative Humidity\n"
            temp[2][1] = "Percent\n"
            self.rh_file.set_header(temp)
        else:
            self.print_center(self.rh_file.name() + \
                                     " found, it will be appended to")



    def calc_rh(self):
        """
            calculates the relative humiditys
        """
        comp_val = 6999
        air_dates = self.at_file[0]
        air_temps = self.at_file[1]
        dew_dates = self.dp_file[0]
        dew_points = self.dp_file[1]
        self.rh_vals = []
        index = 0
        while (index < len(air_dates)):
            rh_val = comp_val
            if not(air_dates[index] == dew_dates[index]):
                errors.set_error_state("Date",
                        "the air temp and dew point dates do not match")
                return
                # how to handle this?
                # ...pandas
            if (air_temps[index] != comp_val and
                dew_points[index] != comp_val):
                denominator = 0.611 * math.exp((17.3 * air_temps[index])
                                 / (air_temps[index] + 237.3))
                numerator = 0.611 * math.exp((17.3 * dew_points[index])
                                / ( dew_points[index] + 237.3))
                rh_val = numerator / denominator * 100
                if rh_val > 100 :
                    rh_val = 6999
            self.rh_vals.insert(index, rh_val)
            index = index + 1

    def main(self):
        """
            the body of the utility
        """
        self.load_files()
        self.calc_rh()
        if self.errors.get_error_state():
            self.errors.print_errors()
            self.exit()

        self.rh_file.set_dates(self.at_file[0])
        self.rh_file[1] = self.rh_vals

        if not self.rh_file.append():
            self.print_center("Old dates indcate no new data to be appended.")
            self.print_center("No data was written.                         ")





if __name__ == "__main__":
    rhu = rh_util()
    rhu.run()






