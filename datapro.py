#!/usr/bin/python -tt
"""
datapro 3.0

IARC data processing project

rawser spicer
created: 2014/08/21
modified: 2014/11/05

        Datapro is a program to proceess the data from a logger site into files
    for each measurement from the site. 

based on datapro v 0.2 by Bob Busey

    version 2014.11.05.1:
        updated load_data_file to work with the new csv_args __getitem__ method,
    the try except block has been removed, which is what the change was designed
    to avoid anyway.
    
    version 2014.10.31.2:
        updated error messege where last date coud not be read to be more 
    helpful and fixed a bug where if the first file failed to load the last 
    date the program would crash

    version 2014.10.31.1:
        fixed error in processing parital data files
        
    version 2014.10.30.1:
        changed some function names
    
    version 2014.10.22.1:
        cleaned up code a bit removing old commented out functions and features
    and added timing features
    
    version 2014.10.20.1:
        add the help

    version 2014.10.15.1:
        optimized the loading of of output files that exist

    version 2014.10.10.1:
        commented out un used code, added minor optimization

    version 2014.10.8.1:  (testing version 1)
        all functionaliy is written and should work, full run bug testing to be
    continued.

"""
import csv_lib.utility as util
from csv_lib.key_file import KeyFile
from csv_lib.param_file import ParamFile
from csv_lib.dat_file import DatFile
from csv_lib.therm_file import ThermFile
import csv_lib.csv_date as csvd
import csv_lib.csv_file as csvf
import csv_lib.equations as eq
import datetime
import os

HELP_STRING = """
Datapro 3.0
help updated: 2014/10/20

        Datapro 3 is a replacemnt for Datapro v2 by Bob Busey. Datapro will
    process data for a site specified by the key file into two column .csv files
    based on each of the measurements for the site. Datapro is capable of
    creating new .csv files or appending to existing ones.

    example usage:
        python datapro.py --key_file=<path_to_key_file>

    flag info:

        --key_file:         <<path_to_file>.txt>
                the key file with information on the data processing directory

        --alt_data_file:    <<path_to_file>.dat> (optional)
                the path to an alternate data file no given in key file

              """

class datapro_v3(util.utility_base):
    """
    this class contains the functions needed for the datapro utility
    """
    def __init__(self):
        """
            sets up datapro
        """
        super(datapro_v3, self).__init__(" Datapro 3.0 " ,
                    ("--key_file",) ,("--alt_data_file",), HELP_STRING)
        self.key_file = "not ready"
        self.param_file = "not ready"
        self.data_file = "not ready"
        self.therm1 = "null"
        self.therm2 = "null"
        self.therm3 = "null"
        self.date_col = []
        self.logger_type = "unknown"
        self.output_directory = {}
        # --- timing ---
        self.timing_bool = True


    def main(self):
        """
        main body of datapro_v3
        """
        self.load_files()
        # --- timing file setup ---
        self.timing_path = self.key_file["output_dir"] + "datapro_runtime.csv"
        # -------------------------
        self.evaluate_errors()
        self.check_directories()
        self.process_dates()
        self.evaluate_errors()
        self.initlize_params()




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
        
        f_name = self.commands["--alt_data_file"]
        if f_name == "":
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
            print self.key_file.lib
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


    def initlize_params(self):
        """
            this function loops over the paramaters that need to be written to
        output files and sets up the file and data processing
        """
        rows = self.param_file.params
        for index in range(len(rows)):
            row = rows[index]
            if row["Data_Type"] == "ignore" or row["Data_Type"] == "datey" or \
               row["Data_Type"] == "dated" or row["Data_Type"] == "dateh" or \
               row["Data_Type"] == "tmstmpcol":
                   continue

            out_name = row["d_element"] + ".csv"
            out_file = csvf.CsvFile(self.key_file["output_dir"] + out_name
                                                                , opti = True)
            out_exists = out_file.exists()
            if out_exists:
                try:
                    last_date = out_file[0][-1]
                except IndexError:
                    file_errors = \
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + \
                    ",file: " + self.key_file["output_dir"] + out_name + \
                    ", cannot read last date" + \
                    " (perhaps there is an extra new line)\n" 
                    error_file = open(self.key_file["error_log_dir"] + \
                                    "I0_read_erros.csv", 'a')
                    error_file.write(file_errors)
                    error_file.close()
                    continue
                if last_date == self.date_col[-1]:
                    continue
            else:
                last_date = datetime.datetime(1000,1,1)
                out_file.set_header(self.generate_output_header(index))
            param_to_process = {"name" : out_name,
                                               "file" : out_file,
                                               "exists" : out_exists,
                                               #~ "element" : row["d_element"],
                                               "index" : index,
                                               "date" : last_date}#,
                                        #~ "Input_Col" : row["Input_Array_Pos"],
                                            #~ "type" : row["Data_Type"]}

            self.process_param(param_to_process)


    def process_param(self, param):
        """
            this function handles a parameter by processing, QC checking and
        saving the file

        arguments:
            param:      (param libary) info on the param to process
        """
        col = self.process_param_data(param["index"], param["date"])
        if len(col) == 0:
            return  # no data processed no need to do QC or save
        col = self.process_param_qc(col, param["index"])
        self.process_param_save(param["file"], col)
        #~ print get_rid_of_this_bad_line_of_code


    def process_param_data(self, index, final_date):
        """
            processes a paramater of data turning it into a column that
        can be outputted

        argumetns:
            index:      (int) index to the param array
            final_date: (datetime) date to process to
        """
        col = []
        ddx = len(self.date_col) - 1 # date index
        array_input_pos = int(self.param_file.params[index]["Input_Array_Pos"])

        ws_index = int(float(self.param_file.params[index]["Coef_3"]))
        for item in reversed(self.data_file[:]):
            if not final_date == datetime.datetime(1000,1,1) \
                                and self.date_col[ddx] <= final_date:
                break
            # ddx -= 1 # for array based data files this will decrement to often 
                       # if left here  mof inside next if statment
            if self.key_file["array_id"] == "-9999" or \
               self.key_file["array_id"] == item[0]:
                ddx -= 1 
                if ws_index != 0:
                    windspeed = item[ws_index]
                else:
                    windspeed = 0

                try:

                    temp = self.process_data_point(item[array_input_pos], index,
                                                    windspeed)
                    col.insert(0, temp)

                except IndexError:
                    continue
        return col


    def process_data_point_therm(self, data_point, index):
        """
            process data if it uses a therm file

        arguments:
            data_point:     (float|string) the data to process
            index:          (int) index to the param array
        """
        try:
            data_point = float(data_point)
        except ValueError:
            return float(self.key_file["bad_data_val"])


        param = self.param_file.params[index]
        d_type = param["Data_Type"]

        if d_type == "therm_1":
            therm_file = self.therm1
        elif d_type == "therm_2":
            d_file = self.therm2
        elif d_type == "therm_3":
            therm_file = self.therm3
        else:
            return float(self.key_file["bad_data_val"])

        therm_idx = therm_file.bin_search(data_point)
        therm_vals = therm_file[therm_idx]

        value = eq.thermistor(data_point, therm_vals.A, therm_vals.B,
                                          therm_vals.C, param["Coeff_4"],
                                          self.ket_file["bad_data_val"])
        return value


    def process_data_point(self, data_point, index, windspeed):
        """
            process the data

        arguments:
            data_point:     (float|string) the data to process
            index:          (int) index to the param array
            windspeed:      (float) windspeed for netrad
        """
        try:
            data_point = float(data_point)
        except ValueError:
            return float(self.key_file["bad_data_val"])
        param = self.param_file.params[index]
        d_type = param["Data_Type"]

        if d_type == "num" or d_type == "net" or d_type == "precip":
            return data_point

        elif d_type == "therm" or d_type == "thermF":
            value = eq.thermistor(data_point, param["Coef_1"], param["Coef_2"],
                                  param["Coef_3"], param["Coef_4"],
                                  self.key_file["bad_data_val"]).result
            if value != float(self.key_file["bad_data_val"]) and \
                                                    d_tpye == "thermF":
                value = value * 9.0 / 5.0 + 32
            return value

        elif d_type == "poly":
            return eq.poly(data_point, param.coefs,
                           self.key_file["bad_data_val"]).result

        elif d_type == "flux":
            return eq.flux(data_point, param["Coef_1"], param["Coef_2"],
                                    self.key_file["bad_data_val"]).result

        elif d_type == "netrad":
            if param["Coef_3"] != 0:
                return eq.netrad(data_point, windspeed,
                                 param["Coef_1"], param["Coef_2"],
                                 self.key_file["bad_data_val"]).result
            else:
                if data_point > 0:
                    constant = 1.045
                else:
                    constant = 1
                return cosntatnt * eq.flux(data_point,
                                    param["Coef_1"], param["Coef_2"],
                                    self.key_file["bad_data_val"]).result

        elif d_type == "rt_sensor":
            return eq.rt_sensor(data_point, param["Coef_1"], param["Coef_2"],
                                param["Coef_3"],
                                self.key_file["bad_data_val"]).result
        elif d_type == "therm_1" or d_type == "therm_2" or d_type == "therm_3":
            return process_data_point_therm(data_point, index)

        else:
            return float(self.key_file["bad_data_val"])


    def process_param_qc(self, data, index):
        """
            check a column
        """
        param = self.param_file.params[index]
        qc_high = float(param['Qc_Param_High'])
        qc_low = float(param['Qc_Param_Low'])
        qc_step = float(param['Qc_Param_Step'])
        bad_val = float(self.key_file["bad_data_val"])
        d_element = param["d_element"]
        date_base = len(self.date_col) - len(data)
        error_log = []

        for index in range(len(data)):
            date = self.date_col[date_base + index]
            if data[index] == bad_val:
                error_log.append(str(date) + ",bad at logger,default," + \
                                    str(data[index]))
                continue

            if not qc_high == 0.0 and data[index] > qc_high:

                error_log.append(str(date) + "qc_high_violation,limit =" \
                                  + str(qc_high) + ',RawDataValue ' + \
                                    str(data[index]))
                data[index] = bad_val
            if not qc_low == 0.0 and data[index] < qc_low:

                error_log.append(str(date) + "qc_high_violation,limit =" \
                                  + str(qc_low) + ',RawDataValue ' + \
                                    str(data[index]))
                data[index] = bad_val


            if qc_step != 0:

                # this tests for the index > 0 first, so if  index == 0
                # the first test will evaulate to false and the test will
                # fail automaticly
                if index > 0 and bad_val != data[index - 1] and \
                    abs(data[index] - data[index - 1]) > qc_step:
                    error_log.append( \
                        str(date) + ",qc_step error,MaxStepDiff " + \
                        str(qc_step) + ",diff " + \
                        str(abs(data[index] - data[index - 1])) +\
                        ',RawDataValue ' + str(data[index]))
                    data[index] = bad_val

        filename = self.key_file["qc_log_dir"].rstrip() + d_element + \
                   '_qaqc_log.csv'

        # are there any errors to write
        if not len(error_log) == 0:
            qc_file = open(filename, 'a')

            for rows in error_log:
                qc_file.write(rows)
                qc_file.write("\n")

        return data

    def process_param_save(self, out_file, data):
        """
        this functions saves a proccessed param to a .csv file
        """
        idx = -1 * len(data)


        out_file.add_dates(self.date_col[idx:])
        out_file.add_data(1,data)

        out_file.append()





if __name__ == "__main__":
    datapro = datapro_v3()
    datapro.run()
