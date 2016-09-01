"""
dat_file.py
rawser spicer
created: 2014/08/27
modified: 2014/12/03

Part of DataPro Version 3

    This class represents the data files used in datapro, table or array types.
It stores each data row in an array, as an array of each value in each row. 
Access is achieved via the [] operator

    version 2015.7.9.1:
        added a tram file option to the setup step
        added the option to set a arbitrary number of header lines in the other
    setupoption

    version 2014.12.3.1:
        blank lines in data file are ignored when reading file now

    version 2014.11.25.1:
        added a set containg the array ids in an array data file or the empty
    set for a table data file

    version 2014.9.8.1:
        added support for "#" type comments in the data files

"""


class DatFile(object):
    """
    This class represents the data files used in datapro
    """
    def __init__(self, file_name, logger_type = "auto"):
        """
            loads the file
            
        arguments:
            file_name:      (string) the file name
            logger_type:    <"auto"|"table"|"array"|"tram"|#> 
                        the type of the logger. "auto" will guess and is set by
                        default. if a # is set it should be in number of lines
                        in the header
        """
        data_file = open(file_name, 'r')
        raw_data = data_file.read()
        data_file.close()
        data = []
        array_ids = [] # for optimizing array files actions 
        for item in raw_data.strip().replace('\r','').split('\n'):
            #is it a blank line or comment
            if len(item) == 0 or item[0] == "#" or item[0] == ',':
                continue
            temp = item.split(',')
            
            data.append(temp)
            array_ids.append(temp[0])
            
        
        if (logger_type == "auto"):
            if not data[0][0].isdigit():
                logger_type = "table"
            else:
                logger_type = "array"
        
        self.col_names = [] 
        if logger_type == "table":
            self.logger_type = "table"
            self.data = data[4:]
            self.array_ids = set() #empty set
        elif logger_type == "array":
            self.logger_type = "array"
            self.data = data
            self.array_ids = set(array_ids) #set of array ids in data fil
        elif logger_type == "tram":
            self.logger_type = "tram"
            self.data = data[4:]
            self.array_ids = set() #empty set
            self.col_names = data[1]
        else:
            self.logger_type = "other"
            self.data = data[int(logger_type):]
            self.array_ids = set() #empty set
 
 
    def __getitem__(self, idx):
        """
            overlaods the __getitem__ function
        
        arguments:
            idx:    (int) the number of the row
        
        returns:
            the array reprenting the requested row
        """
        return self.data[idx]
    
    def getColumn(self, num):
        """
            gets a column from the .dat file
            
        arguments:
            num:    (int) the column number
        
        returns:
            the column
        """
        try:
            self.data[0][num]
        except IndexError:
            raise IndexError, "Column does not exist"
        col = []
        for row in self.data:
            col.append(row[num])
        return col
        
