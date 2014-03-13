"""
CSV Utilities file Module
csv_file.py
Rawser Spicer
created 2014/03/05
modifyed 2014/03/06

    implemtes a class to handel the file io of csv files

    update 2014.3.6.2
         the number of colums in now detrimined by the last row of the header

    update 2014.3.6.1
        added all basic features and doucumentation

"""
import copy
import os
import csv_lib.csv_utilities as csvu
import csv_lib.csv_date as csvd
import numpy as np
#import datetime

def load_info( f_name):
    """
    loads the header, header_length and number of data columns in a file 
    """
    f_stream = open(f_name, "r")
    h_len = 0
    n_cols = 0
    header = []
    while True:
        line = f_stream.readline()
        segs = line.split(',')
        try:
            csvd.string_to_datetime(segs[0])
            break
        except AttributeError:
            header.append(segs)               
        h_len += 1
    n_cols = len(header[-1])
    f_stream.close()
    return n_cols, h_len, header 


class CsvFile:
    """
    CsvFile -- a class to represent csv files in memory
    can be used to open,create,modify,and save csv files   
    """
    def __init__(self, f_name, must_exist = False):
        """
        constructor
        if a file name is provided it will be loaded into the object if it
        exists. if it does not exist it will be created
        f_name - the file name
        """
        self.m_name = ""
        self.m_numcols = 0
        self.m_headlen = 0
        self.m_header = []
        self.m_datacols = []
        self.m_exists = False
        
        if os.path.isfile(f_name):
            self.open_csv(f_name)  
        elif not must_exist:
            self.create(f_name)
        else:
            raise IOError, "file, " + f_name + " was not found"

    def open_csv(self, f_name):
        """
        opens a csv file if it exists
        f_name - the name
        """
        if os.path.isfile(f_name):
            self.m_name = f_name 
            self.m_numcols,  self.m_headlen, self.m_header = \
                                                        load_info(self.m_name)
            self.m_datacols = csvu.load_file_new(self.m_name, self.m_headlen, 
                                                             self.m_numcols)[:]
            self.m_exists = True
        else:
            raise IOError, "file, " + f_name + " was not found"
            
    def create(self, f_name, header = "def,\ndef,def\n"):  
        """
        creates the representation of a csv file with out any major attributes 
        set beyond their default value. 
        a header of "def,\n" will be used if a header is not provided
        f_name - the file name
        header - the header 
        """          
        self.m_name = f_name
        try:
            self.string_to_header(header)
        except TypeError:
            self.m_header = header          
        self.m_headlen = len(self.m_header)  
             
        self.m_numcols = 0           
        self.m_datacols = []            
        self.update_num_cols()
        self.m_exists = False
            
    
    def update_num_cols(self):
        """
        update the number of columns the file has
        """
        self.m_numcols = len(self.m_header[-1])        
        #for index, items in enumerate(self.m_header):
        #    if len(items) > self.m_numcols:
        #        self.m_numcols = len(items) 
        index = len(self.m_datacols) 
        while index < self.m_numcols:
            self.m_datacols.append([])
            index += 1


    def create_data(self, s_date, e_date, t_step, def_val = 0.0):
        """
        with a start and end date as well as a time step create the 
        data section of a csv file with all of the non date values set to 
        def_val. the dates (col 0) will be all timesteps between the start 
        and end 
        s_date - the start date
        e_date - the end date
        t_step - the time step
        def_val - a default value
        """
        dates = []
        temp_arr = []
        dates.append(s_date)
        t_delta = t_step
        while (s_date + t_delta) < e_date:
            dates.append(s_date + t_delta)
            temp_arr.append(def_val)
            t_delta += t_step

        temp_arr.append(def_val)
        self.m_datacols[0] = dates[:]
                
        index = 1
        while index < self.m_numcols:
            self.m_datacols[index] = temp_arr[:]            
            index += 1 

    def __getitem__(self, key):
        """        
        overloaded [] operator
        """
        return copy.deepcopy(self.m_datacols[key])

    def __setitem__(self, key, value):
        """        
        overloaded [] operator
        """ 
        self.m_datacols[key] = value
    
    def __len__(self):
        """
        returns the len of the header and the number of columns
        """
        return ( self.m_numcols)

    def __delitem__(self, key):
        """
        mabey i should delete somthing
        """
        del self.m_datacols[key] 
              

    def header_to_string(self):
        """
        converts the internal list form header to a string
        """
        h_string = ""
        for row in self.m_header:
            for item in row:
                if item[-1:] != '\n':
                    h_string += str(item) + ','
                else:
                    h_string += str(item)
        return h_string

    def string_to_header(self, h_str):
        """
        converts a string to the list form header
        h_str - the string header
        """
        if not isinstance(h_str, str):
            raise TypeError, "in string_to_header, h_str must be a string "
        header = []
        while True:
            line = ""
            while line[-1:] != '\n':
                try:
                    line += h_str[0]               
                    h_str = h_str[1:]
                except IndexError:
                    self.m_header = header
                    return
            segs = line.split(',')
            header.append(segs)
        self.m_header = header

    def data_to_string(self):
        """
        converts the internal data to a string
        """
        data_str = ""
        for index, date in enumerate(self.m_datacols[0]):
            data_str += str(date)
            for values in self.m_datacols[1:]:
                try:
                    data_str += ',' + ("%.2f" % values[index])
                except IndexError:
                    break          
            data_str += '\n'     
        return data_str

    def print_file(self):
        """
        prints the contents of the file to the terminal
        """
        print self.header_to_string()
        print self.data_to_string()    

    def get_dates(self):
        """
        gets the dates column
        """
        return self[0]

    def set_dates(self, new_date_col):
        """
        sets the dates column
        new_date_col = the new dates
        """
        self[0] = new_date_col

    def get_header(self):
        """
        returns the list form of the header
        """
        return copy.deepcopy(self.m_header)        

    def set_header(self, new_header):
        """
        sets the header
        new header the new header 
        """        
        self.m_header = new_header
        self.m_headlen = len(self.m_header)
        self.update_num_cols()

    def save(self, name = ""):
        """
        saves the file 
        name - a new name if you wish to write to a different file
        """
        if name == "" :
            name = self.m_name
        else:
            self.m_name = name
        f_stream = open (name, 'w')
            
        f_stream.write(self.header_to_string())
        f_stream.write(self.data_to_string())
       
        f_stream.close()
        self.m_exists = True

    def append(self, name = ""):
        """
        will append to the end of the data 
        """
        if name == "" :
            name = self.m_name
        else:
            self.m_name = name
     
        if not os.path.exists(name):
            self.save(name)
            return True
        
        temp = CsvFile(name, True)
        last_date = temp[0][-1]
              
        if self[0][-1] <= last_date:
            return False
        index = len(temp[0])
        del temp
        f_stream = open (name, 'a')
        w_str = ""
        while (index < len(self[0])):
            w_str += str(self[0][index])
            col = 1
            while col < self.m_numcols:
                w_str += ',' + ("%.2f" % self[col][index])
                col += 1    
            index += 1
            w_str += "\n"
        f_stream.write(w_str)            
            
        f_stream.close()
        self.m_exists = True
        return True

    def exists(self):
        """
        returns if the file exists at the path provided
        """
        return self.m_exists

    def name(self):
        """Returns the file name"""
        return self.m_name


    def set_name(self, new_name):
        """ change the name associated with the file """
        self.m_name = new_name

    def add_dates(self, new_dates):
        self.add_data(0, new_dates)


    def add_data(self, col, new_data):
        """ adds the new data to the end of column"""
        
        self.m_datacols[col] = np.append(self.m_datacols[col], new_data)
        #print self.m_datacols[col]

