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
from csv_lib.param_file import ParamFile
from csv_lib.dat_file import DatFile



class datapro_v3(util.utility_base):
    def __init__(self):
        """
            sets up datapro
        """
        super(datapro_v3, self).__init__(" Datapro 3.0 " ,
                    ("--key_file",) ,("--alt_data_file",), "help")
        self.key_file = "not ready"
        self.param_file = "not ready"
        self.data_file = "not ready"


    def main(self):
        self.load_files()
        if self.errors.get_error_state():
            self.errors.print_errors()
            self.exit()
        self.check_directories()
        
        
        
    def load_files(self):
        self.load_key_file()
        self.load_param_file()
        self.load_data_file()

        
    def load_key_file(self):
        try:
            self.key_file = KeyFile(self.commands["--key_file"])
        except IOError:
            self.errors.set_error_state("Error", "Key File not found") 
        self.print_center(" Key File Report ", "=")
        print("Station Name:    " + self.key_file["station_name"])
        print("logger type:     " + self.key_file["logger_type"])
        print("input file:      " + self.key_file["input_data_file"])
        print("output dir:      " + self.key_file["output_dir"])
        print("qc log dir:      " + self.key_file["qc_log_dir"])
        print("error log dir:   " + self.key_file["error_log_dir"])
        self.print_center("==", "=")
        print ""
        print ""
    
    
    def load_param_file(self):# (config file)
        try:
            self.param_file = ParamFile( self.key_file["input_data_file"][5:])
        except IOError:
            self.errors.set_error_state("Error", 
                                "Param (config) File not found")
                                
    def load_data_file(self):
        try:
            f_name = self.commands["--alt_data_file"]
        except KeyError:
            f_name = self.key_file["array_based_params_key_file"]

        try:
            self.data_file = DatFile(f_name)
        except IOError:
            self.errors.set_error_state("Error", 
                                "Param (config) File not found")
       
    def check_directories(self):
        pass
        
    def process_data(self):
        pass
    
    def write_out(self):
        pass

if __name__ == "__main__":
    datapro = datapro_v3()
    datapro.run()
