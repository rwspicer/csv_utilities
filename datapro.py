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
from csv_lib.therm_file import ThermFile
import csv_lib.csv_date as csvd
import os



class datapro_v3(util.utility_base):
    """
    this class contains the functions needed for the datapro utility
    """
    def __init__(self):
        """
            sets up datapro
        """
        super(datapro_v3, self).__init__(" Datapro 3.0 " ,
                    ("--key_file",) ,("--alt_data_file",), "help")
        self.key_file = "not ready"
        self.param_file = "not ready"
        self.data_file = "not ready"
        self.therm1 = "null"
        self.therm2 = "null"
        self.therm3 = "null"
        self.date_col = []


    def main(self):
        """
        main body of datapr_v3
        """
        self.load_files()
        if self.errors.get_error_state():
            self.errors.print_errors()
            self.exit()
        self.check_directories()
        self.process_dates()
        
        
    def load_files(self):
        """
        loads the input files
        """
        self.load_key_file()
        if self.errors.get_error_state():
            self.errors.print_errors()
            self.exit()
        self.load_param_file()
        self.load_data_file()
        self.load_therm_files()

        
    def load_key_file(self):
        """
        loads the key file
        """
        try:
            self.key_file = KeyFile(self.commands["--key_file"])
        except IOError:
            self.errors.set_error_state("I/O Error", "Key File not found") 
            return
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
        """
        loads the paramater (config) file
        """
        try:
            self.param_file = \
                        ParamFile( self.key_file["array_based_params_key_file"])
        except IOError:
            self.errors.set_error_state("I/O Error", 
                                "Param (config) File not found")
                                
    def load_data_file(self):
        """
        loads the data file
        """
        try:
            f_name = self.commands["--alt_data_file"]
        except KeyError:
            f_name = self.key_file["input_data_file"][5:]

        try:
            self.data_file = DatFile(f_name)
        except IOError:
            self.errors.set_error_state("I/O Error", 
                                "Data File not found")
       
    def load_therm_files(self):
        """
        loads the therm files if any
        """
        if self.key_file['therm1'] != "null":
            try:
                therm1 = ThermFile(self.key_file['therm1'])
            except IOError:
                self.errors.set_error_state("I/O Error", 
                                            "thermistor file 1 not found")
        
        if self.key_file['therm2'] != "null":
            try:
                therm2 = ThermFile(self.key_file['therm2'])
            except IOError:
                self.errors.set_error_state("I/O Error", 
                                            "thermistor file 2 not found")
        
        if self.key_file['therm3'] != "null":
            try:
                therm3 = ThermFile(self.key_file['therm3'])
            except IOError:
                self.errors.set_error_state("I/O Error", 
                                            "thermistor file 3 not found")
        
       

    def check_directories(self):
        """
        checks for and creates missing directories
        """
        if not os.path.exists(self.key_file["output_dir"]):
            os.mkdir(self.key_file["output_dir"])
        if not os.path.exists(self.key_file["qc_log_dir"]):
            os.mkdir(self.key_file["qc_log_dir"])
        if not os.path.exists(self.key_file["error_log_dir"]):
            os.mkdir(self.key_file["error_log_dir"])
        
    
    
    def process_dates(self):
        """
            This function creates the date column for the output csv files
        from the time stamp column in tabel type data file 
        """
        for elems in self.param_file.params:
            if elems["Data_Type"] == "tmstmpcol":
                i_pos = int(elems["Input_Array_Pos"])
                break
        
        for rows in self.data_file[:]:
            self.date_col.append(csvd.string_to_datetime(rows[i_pos]))



    def process_data(self):
        pass
    
    def write_out(self):
        pass

if __name__ == "__main__":
    datapro = datapro_v3()
    datapro.run()
