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
import datetime
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
        self.logger_type = "unknown"


    def main(self):
        """
        main body of datapro_v3
        """
        self.load_files()
        self.evaluate_errors()
        self.check_directories()
        self.process_dates()
        self.evaluate_errors()
        

        
    def load_files(self):
        """
        loads the input files
        """
        self.load_key_file()
        self.logger_type = self.key_file["logger_type"].upper()
        if "CR10X" == self.logger_type:
            self.logger_type = "ARRAY"
        self.evaluate_errors()
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
            #TODO: check for "file:///" deal
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
        
        #is there a third thermistior file
        try:
            self.key_file['therm3']
        except:
            return
            
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
            os.makedirs(self.key_file["output_dir"])
        if not os.path.exists(self.key_file["qc_log_dir"]):
            os.makedirs(self.key_file["qc_log_dir"])
        if not os.path.exists(self.key_file["error_log_dir"]):
            os.makedirs(self.key_file["error_log_dir"])
        
    
    def process_dates(self):
        if self.logger_type == "ARRAY":
            self.process_dates_array()
        elif self.logger_type == "TABLE":
            self.process_dates_table()
        else:
            self.errors.set_error_state("Runtime Error", "logger type unknown")
    
    def process_dates_array(self):
        count = 0 
        year_col = -1 
        day_col = -1
        hour_col = -1
        for elems in self.param_file.params:
            if count == 3:
                break
            print elems["Data_Type"]
           
            if elems["Data_Type"] == "datey":
                year_col = int(elems["Input_Array_Pos"])
                count += 1
            if elems["Data_Type"] == "dated":
                day_col = int(elems["Input_Array_Pos"])
                count += 1
            if elems["Data_Type"] == "dateh":
                hour_col = int(elems["Input_Array_Pos"])
                count += 1
        
        if day_col == -1 or hour_col == -1:
            self.errors.set_error_state("Runtime Error", "date column error")
            print day_col, hour_col
            return
    
    
        for item in self.data_file[:]:
            if int(item[0]) == int(self.key_file["array_id"]):
                if year_col == -1:
                    year = datetime.datetime.now().year
                else:
                    year = item[year_col]
                self.date_col.append(csvd.julian_to_datetime(year, 
                                        item[day_col], item[hour_col]))
    
    def process_dates_table(self):
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
   # print datapro.date_col
