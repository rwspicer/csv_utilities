#!/usr/bin/python
"""
arraykeygen.py
Rawser Spicer
Created: 2014/17/11
Modified: 2014/17/11

        this utility is for taking an array based param file for datapro and 
    generating a key file if the key file is missing. It requires that the Key
    file be in the format  <station name>_params_<array ID>-<arrays>.csv
    
    
    version 2014.11.17.2:
        fixed --out_dir flag
    
    version 2014.11.17.2:
        fixed error with array_id
    
    version 2014.11.17.1:
        initial version
    
"""
import csv_lib.utility as util

HELP_STRING = """
        This utility will generate a key file for datapro 3.0 based on an array 
    param file for datapro 3.0. 
    
    example usage:
        python arraykeygen.py --param_file=<path_to_file> --datapro_output_root=
        <path_to_directory> --data_file=<path_to_data_file>
    
    NOTE: absolute paths will have best results
    
    flag info:
        --param_file:               <<path_to_file>/<sitenme>_array_<tag>_params
                                    _<array ID>-<arrays>.csv>
                        the param file for an array based data file
                        ex: <path>/skookum_array_met_params_118-12.csv
                        
        --datapro_output_root:      <path_to_directory>
                        the path to the directory for the datapro outputs
                        
        --data_file:                <<path_to_file>/<fuilename>>
                        the datafile for datapro
        --out_dir:                  <path_to_directory> (optional)
                        path to save location for key file, defaults to current
                    dir
                    
        --therm1, --therm2, --therm3:   <path_to_thermfiles> (optional)
                        thermistor files for datapro, defaults to "null"
        --bv:                           <Integer>
                        bad value used  by datapro, defaults to 6999
        

              """

class ArrayKenGen(util.utility_base):
    def __init__(self):
        super(ArrayKenGen, self).__init__(" Array Key File Generator " ,
                    ("--param_file", "--datapro_output_root", "--data_file") ,
                    ("--out_dir", "--therm1", "--therm2", "--therm3" , "--bv"),
                     HELP_STRING)
        self.param_file = ""
        self.output_file = ""
        self.working_root = "./"
        self.site_name = "name"
        self.arrays = ""
        self.array_ID = ""
 
        
    def main(self):
        self.param_file = self.commands["--param_file"]
        
        self.parse_param_file_name()
        self.working_root = self.commands["--datapro_output_root"] +\
                            self.site_name[:self.site_name.find('_')] + "/"
        self.write_key_file()
        
        
    def parse_param_file_name(self):
        p_file = self.param_file[self.param_file.rfind("/")+1:]
        pidx = p_file.find("_params_")
        pidx_offset = pidx + len("_params_")
        didx = p_file.find("-")
        self.site_name = p_file[:pidx].replace("_array","")
        self.array_ID = p_file[pidx_offset:didx]
        self.arrays = p_file[didx + 1:p_file.find(".")]
        
    def write_key_file(self):
        nl = "\n"
        out_str = "# key file generated from param file" + nl
        out_str +=  "station_name = " + self.site_name.replace("_", " -- ") + nl
        out_str += "logger_type = array" + nl
        out_str += "arrays = " + self.arrays + nl
        out_str += "array_id = " + self.array_ID + nl
        out_str += nl
        out_str += "# input file info" + nl
        out_str += "input_data_file = " + self.commands["--data_file"] + nl
        out_str += "array_based_params_key_file = " + self.param_file + nl
        out_str += nl
        out_str += "# therm file info" + nl
        self.commands.return_func = self.therm_rtn
        out_str += "therm1 = " + self.commands["--therm1"] + nl
        out_str += "therm2 = " + self.commands["--therm2"] + nl
        out_str += "therm3 = " + self.commands["--therm3"] + nl
        self.commands.return_func = self.commands.stringify
        out_str += nl
        out_str += "# Working Directories" + nl
        out_str += "output_dir = " + self.working_root + "outputs/" + nl
        out_str += "qc_log_dir = " + self.working_root + "qc/" + nl
        out_str += "error_log_dir = " + self.working_root + "error/" + nl
        out_str += nl
        out_str += "# bad data val" + nl
        self.commands.return_func = self.bv_rtn
        out_str += "bad_data_val = " + self.commands["--bv"] + nl
        
        self.commands.return_func = self.commands.stringify
        out_dir = self.commands["--out_dir"]
        
        if out_dir == "":
            out_dir = "./"
        
            
        p_file = self.param_file[self.param_file.rfind("/")+1:]
        outfile = open (out_dir + p_file.replace("params", "key"). \
                        replace(".csv", ".txt"), 'w')
        outfile.write(out_str)
        outfile.close()
        print "key file: " + out_dir + p_file 
        
    def therm_rtn(self, value):
        if value == "":
            value = "null"
        return str(value)
        
    def bv_rtn(self, value):
        if value == "":
            value = "6999"
        return str(value)
        
        
        

if __name__ == "__main__":
    u = ArrayKenGen()
    u.run()
    
    
    
