#!/usr/bin/python -tt

"""
datapro 3

IARC data processing project

rawser spicer
created: 2014/08/21
modified: 2014/08/21

based on datapro v 0.2 by Bob Busey

"""
import csv_lib.utility as util
from csv_lib.key_file import KeyFile


#alt data file ??????

class datapro_v3(util.utility_base):
    def __init__(self):
        """
            sets up datapro
        """
        super(datapro_v3, self).__init__("Datapro 3" ,
                    ("--key_file",) ,("--alt_data_file",), "help")
        self.key_file = "not ready"
        self.param_file = "not ready"
        self.data_file = "not ready"


    def main(self):
        self.load_files()
        if self.errors.get_error_state():
            self.errors.print_errors()
            self.exit()
        
        #read confing files
        
        
    def load_files(self):
        self.load_key_file()
        self.load_param_file()
        
    def load_key_file(self):
        try:
            self.key_file = KeyFile(self.commands["--key_file"])
        except IOError:
            self.errors.set_error_state("Error", "Key File not found") 
    
    def load_param_file(self):# (config file)
        try:
            self.param_file = open("abc")
        except IOError:
            self.errors.set_error_state("Error", 
                                "Param (config) File not found")
        
    def process_data(self):
        pass
    
    def write_out(self):
        pass

if __name__ == "__main__":
    datapro = datapro_v3()
    datapro.run()
