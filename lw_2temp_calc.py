#!/usr/bin/python -tt
"""
Simple Utility for Longwave Radiation conversion to temperature for QA purposes
rawser spicer & Bob Busey
created: 2017/10/20
modified:


"""

import numpy as np
from csv_lib.dat_file import DatFile
from csv_lib.utility import utility_base
from csv_lib.csv_file import CsvFile
from datetime import datetime
import math as Math

HELP = """
    Simple Utility to make a time series of temperature from long wave radiation data
    to allow for direct comparison with other variables like skin temperature & air temperature.

    example usage:
    >> python lw_2temp_calc.py --infile=<.csv file> --outfile=<.csv file>


    flags:
    --infile
        the input .csv file

    --outfile
        the output .csv file


"""


class LW_Convert(utility_base):
    """
        a utility to for radiation to temperature conversions
    """
    def __init__(self):
        """
             Sets up utility

        Preconditions:
            none
        Postconditions:
            utility is ready to be run
        """
        super(LW_Convert, self).__init__(" LW_Convert " ,
                    ("--infile", "--outfile") ,
                    ( ),
                    HELP)


    def main(self):
        """
        main body of utiliy.

        Preconditions:
            utility setup
        Postconditions:
            utility is run
        """
        # set up
        data = DatFile(self.commands["--infile"],"4")
        columns = [data.getColumn(0),
                   np.array(data.getColumn(1)).astype(float)]
        # test out put
        out_file = CsvFile(self.commands["--outfile"], opti = True)
        last_date = datetime(1000,1,1)
        if not out_file.exists():
            fd = open(self.commands["--infile"])
            first_line = fd.read().split(",")[0:2]
            first_line[1] += "\n"
            out_file.set_header([ first_line,
                                  ("timestamp", "LW Temperature\n"),
                                  ("","Degrees Celsius\n"),
                                  ("","Avg\n")])
        else:
            last_date = out_file[0][-1]
        temperature_vals = []
        temperature_dates = []
        idx = 0
        while idx < len(columns[0]):
            compVal = columns[0][idx]
            # I'm not sure what this does...
            if datetime.strptime(compVal,'"%Y-%m-%d %H:%M:%S"') <= last_date:
                idx = idx + 1
                continue
            # this point is where the magic happens.
            raw_val = float(columns[1][idx])
            if raw_val == 6999.0 :
                temperature_vals.append(6999.0)
            else:
                temperature = (raw_val / 5.67e-8) ** 0.25 - 273.15
                temperature_vals.append(temperature)
            temperature_dates.append(datetime.strptime(compVal,'"%Y-%m-%d %H:%M:%S"'))
            idx= idx+1
        # save
        out_file.add_dates(temperature_dates)
        out_file.add_data(1,temperature_vals)
        out_file.append()


if __name__ == "__main__":
    LW_Convert().run()
