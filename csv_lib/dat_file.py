"""
dat_file.py
rawser spicer
created: 2014/08/27
modified: 2014/09/08

Part of DataPro Version 3

    This class represents the data files used in datapro, table or array types.
It stores each data row in an array, as an array of each value in each row. 
Access is acheived via the [] operator

    version 2014.9.8.1:
        added suppoer for "#" type comments in the data files

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
        for item in raw_data.strip().replace('\r','').split('\n'):
            if item[0] == "#":
                continue
            data.append(item.split(','))
            
        if (logger_type == "auto"):
            if not data[0][0].isdigit():
                logger_type = "table"
            else:
                logger_type = "array"
                
        if logger_type == "table":
            self.logger_type = "table"
            self.data = data[4:]
        elif logger_type == "array":
            self.logger_type = "array"
            self.data = data

    def __getitem__(self, idx):
        """
            overlaods the __getitem__ function
        
        arguments:
            idx:    (int) the number of the row
        
        returns:
            the array reprenting the requested row
        """
        return self.data[idx]
    
    
        
