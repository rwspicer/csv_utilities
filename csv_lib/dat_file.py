"""
dat_file.py
rawser spicer
created: 2014/08/27
modified: 2014/12/03

Part of DataPro Version 3

    This class represents the data files used in datapro, table or array types.
It stores each data row in an array, as an array of each value in each row. 
Access is acheived via the [] operator

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
            logger_type:    <"auto"|"table"|"array"> the type of the logger.
                            "auto" will guess and is set by default
        """
        data_file = open(file_name, 'r')
        raw_data = data_file.read()
        data_file.close()
        data = []
        array_ids = [] # for optimizing array files actions 
        for item in raw_data.strip().replace('\r','').split('\n'):
            #is it a blank line or comment
            if len(item) == 0 or item[0] == "#":
                continue
            temp = item.split(',')
            data.append(temp)
            array_ids.append(temp[0])
            
        if (logger_type == "auto"):
            if not data[0][0].isdigit():
                logger_type = "table"
            else:
                logger_type = "array"
                
        if logger_type == "table":
            self.logger_type = "table"
            self.data = data[4:]
            self.array_ids = set() #empty set
        elif logger_type == "array":
            self.logger_type = "array"
            self.data = data
            self.array_ids = set(array_ids) #set of array ids in data file

    def __getitem__(self, idx):
        """
            overlaods the __getitem__ function
        
        arguments:
            idx:    (int) the number of the row
        
        returns:
            the array reprenting the requested row
        """
        return self.data[idx]
    
    
        
