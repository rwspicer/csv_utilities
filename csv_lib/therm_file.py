"""
dat_file.py
rawser spicer
created: 2014/09/03
modified: 2014/09/23

Part of DataPro Version 3

    This class represents the thermistor files used in datapro, the file creates
a table of rows with the values accessable as class varibles

"""

class ThermVals(object):
    """
    this represents a set of thermistor values
    """
    def __init__(self, res, temp, a, b, c):
        """
        initilizes values
        """
        self.resistance = float(res)
        self.temperature = float(temp)
        self.A = float(a)
        self.B = float(b)
        self.C = float(c)


class ThermFile(object):
    """
    this class repesents a thermistor file
    """
    def __init__(self, f_name):
        """ 
        loads the file
            
        arguments:
            file_name:      (string) the file name
        """
        self.name = "unnamed"
        self.standard = "unknown"
        self.table = []
        self.create_table(f_name)
        
    def create_table(self, f_name):
        """ Function doc """
        therm_file = open(f_name, "r")
        text = therm_file.read()
        therm_file.close()
        
        text = text.split('\n')
        self.name = text[0].split(",")[0]
        self.standard = text[0].split(",")[1]
        text = text[2:]
        for row in text:
            if row == "":
                continue
            cells = row.split(',')
            self.table.append(ThermVals(cells[0], cells[1], cells[2], 
                                                  cells[3], cells[4]))
    def __getitem__(self, idx):
        """
            overlaods the __getitem__ function
        
        arguments:
            idx:    (int) the number of the row
        
        returns:
            the array reprenting the requested row
        """
        return self.table[idx]
        
        
        
        
        
