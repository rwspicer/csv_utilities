"""
Tram Transformation Utility 
rawser spicer
created: 2015/07/09
modified: 2015/07/09
    
     a utility to transform a tram .dat file into .csv files.
"""
# Imports ______________________________________________________________________
from csv_lib.dat_file import DatFile
from csv_lib.csv_file import CsvFile
import datetime


# Classes ______________________________________________________________________
class TramTransform (object):
    """
    this class is for breaking the tram data in to separate files
    """
    def __init__ (self, fName):
        """
        set up class
        
        Preconditions:
            file 'fname' should exist'
        Postconditions: 
            the other functions may be run
        """
        self.inData = DatFile(fName,'tram')
        self.outData = {}

    def transform (self):
        """
        transform the data
        
        Preconditions:
            inData should have data
        Postcondidions:
            outData is a library of sets of rows for each variable in the 
        inData
        """
        dateCol = self.inData.getColumn(0)
        countCol = self.inData.getColumn(2)
        colLib = {}
        idx = 3
        while True:
            try:
                colLib[self.inData.col_names[idx]]= self.inData.getColumn(idx)
                idx +=1
            except IndexError:
                break
        for key in self.inData.col_names[3:]:
            print key
            #~ print colLib[key][:10]
            rows = []
            start = 0
            last = 0
            for idx in range(len(countCol)):
                if int(countCol[idx]) < int(countCol[last]) and idx != start:
                    date = datetime.datetime.strptime(dateCol[start][:13],
                                            "%Y-%m-%d %H")
                    if start == 0:
                        row = colLib[key][start:idx]
                    else:
                        row = colLib[key][start-1:idx]
                    row.insert(0,date)
                    #~ print row
                    rows.append(row)
                    start = idx +1

                last = idx
                #~ if idx == 200:
                    #~ break
            end = colLib[key][start-1:]
            date = datetime.datetime.strptime(dateCol[start][:13],
                                            "%Y-%m-%d %H")
            end.insert(0,date)
            rows.append(end)
            self.outData[key] = rows

    def save (self, outDir):
        """
        Save the output files.
        
        Pre:
            self.transform sould have been called.
            outDir needs to exist
        Post:
            Files for each variable will be saved or updated
        """
        for key in self.inData.col_names[3:]:
            data = self.outData[key]
            outFile = CsvFile(outDir+key+'.csv', opti = True)
            if not outFile.exists():
                cols = range(1,len(data[0]))

                cols.insert(0,'TIMESTAMP')
                #~ print cols
                for i in range(len(cols)):
                    cols[i] = str(cols[i])
                cols[-1]+='\n'
                outFile.set_header([('TOA5','ngee-tram','CR3000','8379',
                                    'CR3000.Std.25','CPU:cart6runzt.CR3',
                                    '46105','Radiation\n'),
                                    cols])
            else:
                last_date = outFile[0][-1]

            for idx in range(len(data[0])):
                col = []
                for row in data:
                    try:
                        col.append(row[idx])
                    except IndexError:
                        col.append('')
                        continue
                outFile.add_data(idx,col)
            outFile.append()


# Utility Help String __________________________________________________________
HELP = """
    This Utility is for splinting out a a tram .dat file into csv files for
each variable in the file 
    
    example usage:
    >> python tramTransform.py --inFile=<.datFile> --outDir=<directory>
    
    Flags:
        --inFile
            The tram .dat file
        --outDir
            a directory to save outputs to
""" 


# Utility ______________________________________________________________________
import csv_lib.utility as util
class TramTransUtil(util.utility_base):
    """
    This utility allows data to be added to an imiq table.
    """
    def __init__(self):
        """
        Sets up utility

        Preconditions:
            none
        Postconditions:
            utility is ready to be run
        """
        super(TramTransUtil, self).__init__(" TramTranform " ,
                    ("--inFile", "--outDir" ) ,
                    (),
                    HELP)

    def main (self):
        """
        main body of utiliy. 
        
        Preconditions:
            utility setup
        Postconditions:
            utility is run
        """
        tt = TramTransform (self.commands["--inFile"])
        tt.transform()
        tt.save(self.commands["--outDir"])


# Run Utility __________________________________________________________________
if __name__ == "__main__":
    TramTransUtil().run()
