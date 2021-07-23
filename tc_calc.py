#!/usr/bin/python -tt
"""
Thermal conductivity Calculator
rawser spicer
created: 2015/06/10
modified: 2015/06/11

     a utility to calcualte the thermal conductivity
"""
from scipy.stats import linregress
import numpy as np
from csv_lib.dat_file import DatFile
from math import pi
from csv_lib.utility import utility_base
from csv_lib.csv_file import CsvFile
from datetime import datetime

HELP = """
    calculates thermal conductivity from a .dat file

    example usage:
    >> python tc_calc.py --infile=<.dat file> --outfile=<.csv file>
    --timecol=<#> --tempcol=<#>

    flags:
    --infile
        the input .dat file

    --outfile
        the output .csv file

    --timecol
        0 based index to the time column

    --tempcol
        0 based index to the trise temperature column

    --powercol
        0 based index to the power column

"""


class CalcK(utility_base):
    """
        a utility to calcualte the thermal conductivity
    """
    def __init__(self):
        """
             Sets up utility

        Preconditions:
            none
        Postconditions:
            utility is ready to be run
        """
        super(CalcK, self).__init__(" CalcK " ,
                    ("--infile", "--outfile", "--timecol", "--tempcol") ,
                    ("--powercol", ),
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
        timeC = int(self.commands["--timecol"])
        tempC = int(self.commands["--tempcol"])
        powerC = self.commands["--powercol"]
        print('   T Col = ', tempC, '    Power Col = ', powerC)
        columns = [data.getColumn(0),
                   np.array(data.getColumn(timeC)).astype(float),
                   np.array(data.getColumn(tempC)).astype(float)]
        if powerC != "":
            powerC = int(powerC)
            columns.append(np.array(data.getColumn(powerC)).astype(float))

        # test out put
        out_file = CsvFile(self.commands["--outfile"], opti = True)
        last_date = datetime(1000,1,1)
        if not out_file.exists():
            fd = open(self.commands["--infile"])
            first_line = fd.read().split(",")[0:2]
            first_line[1] += "\n"
            out_file.set_header([ first_line,
                                  ("timestamp","k\n"),
                                  ("","w/mk\n"),
                                  ("","Smp\n")])
        else:
            # last date of the output file
            last_date = out_file[0][-1]


        # process k
        k_vals = []
        k_dates = []
        idx = 0
        while idx < len(columns[0]):
            compVal = columns[0][idx]
            begin = idx
            end = idx
            try:
                while compVal == columns[0][idx]:
                    idx += 1
                    end = idx
            except:
                pass
            if datetime.strptime(compVal,'"%Y-%m-%d %H:%M:%S"') <= last_date:
                # fast forward through the data file till end.
                continue

            temp_k = 0.
            if powerC == "":
                temp_k = self.calc_K( columns[1][begin:end], columns[2][begin:end] )
            else:
                temp_k = self.calc_K(columns[1][begin:end],
                                          columns[2][begin:end],
                                          columns[3][begin:end])
            # super simple checking... should add this to a qc log at some point...
            if temp_k < 0. :
                temp_k = 6999.
            elif temp_k > 11. :
                temp_k = 6999.
            k_vals.append(temp_k)
            k_dates.append(datetime.strptime(compVal,'"%Y-%m-%d %H:%M:%S"'))

        # save
        out_file.add_dates(k_dates)
        out_file.add_data(1,k_vals)

        out_file.append()


    def calc_K(self, time, trise, power = 2.6):
        """
            Calculates the thermal conductivity

        Arguments
            Time: an array of times
            trise: an array of temperatus
            Power: a arrary of power values

        Returns the thermal conductivity
        """
        Rheater = 70# aproxmaite #np.array([70.0, 70.0, 70.0, 70.0, 69.2, 69.0])
        Rref = 1# aproxmaite # np.array([1.0, 1.0, 1.0, 1.032, 1.023, 1.019])
        #print dateCol[:10]
        Eref = (power/1041.5)**(.5)
        # df = np.diff(columns[0]) / np.diff(columns[6])
        q = ((np.mean(Eref)**2)/(Rref**2) )*(Rheater*(100.0/6))
        slope = linregress(np.log(time),trise)[0]
        return q/(4*pi*slope)



if __name__ == "__main__":
    CalcK().run()
