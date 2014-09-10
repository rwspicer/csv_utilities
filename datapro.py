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
import csv_lib.csv_file as csvf
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
        self.output_directory = {}


    def main(self):
        """
        main body of datapro_v3
        """
        import time
        self.load_files()
        self.evaluate_errors()
        self.check_directories()
        self.process_dates()
        self.evaluate_errors()
        self.pre_process_data()
        

        
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
            f_name = self.key_file["input_data_file"].replace("file:","")

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
        """
            this function handles the processing of dates, by deciding which 
        type of file is being used
        """
        if self.logger_type == "ARRAY":
            self.process_dates_array()
        elif self.logger_type == "TABLE":
            self.process_dates_table()
        else:
            self.errors.set_error_state("Runtime Error", "logger type unknown")
    
    def process_dates_array(self):
        """
            process the dates in array type files
        """
        count = 0 
        year_col = -1 
        day_col = -1
        hour_col = -1
        for elems in self.param_file.params:
            if count == 3:
                break
           
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

    def pre_process_data(self):
        """
            preforms setup steps required for data processing
        """
        self.setup_output_files()
        
    def setup_output_files(self):
        """
            sets up the out put files 
        """
        self.setup_output_directory()
        for key in self.output_directory.keys():
            curr_file = self.output_directory[key]
            if not curr_file["exists"]:
                header = self.generate_output_header(curr_file["index"])
                curr_file["file"].set_header(header)
                

    def setup_output_directory(self):
        """
            sets up a directory of output files needing to be writted or 
        modified
        """
        rows = self.param_file.params
        for index in range(len(rows)):
            row = rows[index]
            if row["Data_Type"] == "ignore" or row["Data_Type"] == "datey" or \
               row["Data_Type"] == "dated" or row["Data_Type"] == "dateh" or \
               row["Data_Type"] == "tmstmpcol":
                   continue
            out_name = row["d_element"] + ".csv"
            out_file = csvf.CsvFile(self.key_file["output_dir"] + out_name)
            out_exists = out_file.exists()
            
            self.output_directory[out_name] = {"name" : out_name,
                                               "file" : out_file,
                                               "exists" : out_exists,
                                               "element" : row["d_element"],
                                               "index" : index}
        
    def generate_output_header(self, idx):
        """
            generats a header for an output file given an index to a row in the
        paramater file
        
        arguments:
            idx:    (int) a row index to the param_file
            
        returns:
            a header list
        """
        row = self.param_file.params[idx]
        return [["TOA5", self.key_file["station_name"], 
                        self.key_file["logger_type"] + '\n'],
                ["TimeStamp", row["Output_Header_Name"] + '\n'],
                ["", row["Output_Header_Name"] + '\n'],
                ["", row["Output_Header_Measurment_Type"] + '\n']]
    
    def write_out(self):
        pass

if __name__ == "__main__":
    time_code = "no"
    if time_code == "ave":
        import time
        total = 0 
        tries = 10
        for idx in range(tries):
            start = time.time()
            datapro = datapro_v3()
            datapro.run()
            end = time.time()
            total += (end - start)
        print total/tries
    elif time_code == "once":
        import time
        start = time.time()
        datapro = datapro_v3()
        datapro.run()
        end = time.time()
        print (end - start)
    else:
        datapro = datapro_v3()
        datapro.run()
        
    #~ print datapro.output_directory
    #~ print datapro.date_col
