"""
CSV Utilities file Module
csv_file.py
Rawser Spicer
created 2014/03/05
modified 2014/11/06

    Implements a class to handle the file IO of .csv files.
 
    version 2014.11.6.1:
        updated output format of dates
    
    version 2014.10.24.1:
        changed over the apped_new function to append. removed old append 
    function. fixed error where header folowed by a blank line would cause 
    crashes

    version 2014.10.23.1:
        added append_new function -- should replace appened after testing
    
    version 2014.10.22.2:
        fixed issues in the append and optimized load functions where a header 
    with no data caused issues 

    version 2014.10.22.1:
        read/writen data can now be in string or float format

    version 2014.10.15.1
        added an optimized load mode that will olny load the last line of the 
    csv file in to the object.

    version 2014.9.12.1
        added new functionailty to load data    

    version 2014.7.30.1
        improved the documentation

    version 2014.3.6.2
        the number of colums in now detrimined by the last row of the header

    version 2014.3.6.1
        added all basic features and doucumentation

"""
#import copy
import os
import csv_lib.csv_utilities as csvu
import csv_lib.csv_date as csvd
import numpy as np
import datetime

def load_info(f_name):
    """
    loads the header, header_length and number of data columns in a file

    arguments:
        f_name:     <*.csv> (string) the name of the file

    return values:
        n_cols:     (int) the number of columns
        h_len:      (int) the number of rows in the header
        header:     (((string) list) list) a list of the list of the strings in
                each "cell" of the header
    """
    f_stream = open(f_name, "r")
    h_len = 0
    n_cols = 0
    header = []
    while True:
        line = f_stream.readline()
        if line == "" or line == "\n":
            break
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

    notes:
        In this class the headers are represented as a list of lists of strings
    representing each "cell" in the header(ie [["title",""],["col 1", "col 2"]])
    The class also has functions to convert between that format and a string
    format (ie."title,\ncol 1,col 2\n" ) and some functions will take either
    type as an argumet.
    """
    def __init__(self, f_name, must_exist = False, opti = False):
        """
            constructor
            if a file name is provided it will be loaded into the object if it
        exists. if it does not exist it will be created

        arguments:
            f_name:     <*.csv> (string) the file name
            must_exist: <True|False> (bool) dose the file have to exist for the
                    class to be created

        execptions:
            IOError: if (must_exist == true) and file not found
        """
        self.m_name = ""
        self.m_numcols = 0
        self.m_headlen = 0
        self.m_header = []
        self.m_datacols = []
        self.m_exists = False
        self.m_opti = opti
        self.m_last_init_date = datetime.datetime(1,1,1) # first date possible
                                                    # will allow append to work
                                                    # if all data needs to be
                                                    # written

        if os.path.isfile(f_name):
            self.open_csv(f_name)
        elif not must_exist:
            self.create(f_name)
        else:
            raise IOError, "file, " + f_name + " was not found"


    def open_csv(self, f_name):
        """
            opens a csv file

        arguments:
            f_name:     <*.csv> (string) the file name

        execptions:
            IOError: if file not found
        """
        
        if os.path.isfile(f_name):
            self.m_name = f_name
            self.m_numcols,  self.m_headlen, self.m_header = \
                                                        load_info(self.m_name)
                
            if self.m_opti == True:
                self.load_csv_file_opti()
            else:    
                self.load_csv_file()            
        
            #self.m_datacols = csvu.load_file_new(self.m_name, self.m_headlen,
            #                                                 self.m_numcols)[:]
            self.m_exists = True
        else:
            raise IOError, "file, " + f_name + " was not found"


    def load_csv_file(self):
        """
            loads a csv file replaces the csv_utitlies version
        """
        f_stream = open(self.m_name, "r")   
        f_text = f_stream.read()
        f_stream.close()
        rows = f_text.replace("\r","").split("\n")

        

        for idx in range(self.m_numcols):
            self.m_datacols.append([])

        
        
        if len(rows) == self.m_headlen:
            return

       
        for item in rows[self.m_headlen:]:
            if item == "":
                continue
            cells = item.split(",")
            for col in range(len(cells)):
                if col == 0:
                    self.m_datacols[col].\
                        append(csvd.string_to_datetime(cells[col]))
                else:
                    try:
                        self.m_datacols[col].append(float(cells[col]))
                    except ValueError:
                        self.m_datacols[col].append(str(cells[col]))
        #store last date in the file
        try:
            self.m_last_init_date = self.m_datacols[0][-1]
        except IndexError:
            pass
            
    def load_csv_file_opti(self):
        """
        a faster load file
        """
        for idx in range(self.m_numcols):
            self.m_datacols.append([])
            
        f_stream = open(self.m_name, "rb")
        f_stream.seek(-2,2)
        while f_stream.read(1) != "\n":
            f_stream.seek(-2,1)
        line = f_stream.readline()
        if line.strip() == "":
            return
        if line[:line.find(',')] == self.m_header[-1][0]:
            return    
        cells = line.split(",")
        for col in range(len(cells)):
            if col == 0:
                self.m_datacols[col].append(csvd.string_to_datetime(cells[col]))
            else:
                self.m_datacols[col].append(float(cells[col]))
        f_stream.close()
        #store last date in the file
        try:
            self.m_last_init_date = self.m_datacols[0][-1]
        except IndexError:
            pass
        
    def create(self, f_name, header = "title,\ncol 1,col 2\n"):
        """
            creates the representation of a csv file with out any major
        attributes set beyond their default value. The default header is an
        example of a two line two column header.

        arguments:
            f_name:     <*.csv> (string) the file name
            header:     (string) or (((string)list)list) the informattion for
                    the header.
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
            detrimines the numver of columns the file has.
        """
        self.m_numcols = len(self.m_header[-1])
        #for index, items in enumerate(self.m_header):
        #    if len(items) > self.m_numcols:
        #        self.m_numcols = len(items)
        index = len(self.m_datacols)
        while index < self.m_numcols:
            self.m_datacols.append([])
            index += 1

    #todo: figure out type of s_date, e_date, and t_step. Probably datetime.datetime and datetime.tiemdelata
    def create_data(self, s_date, e_date, t_step, def_val = 0.0):
        """
            Creates a timestamp column with timesteps between the start time
        and end time seperated by the time step. A second column is alo created
        to be the same length with all values set to the default value.

        arguments:
            s_date:     () the start date
            e_date:     () the end date
            t_step:     () the time step
            def_val:    (any type) a default value
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


    #todo fix theses up to make them safer
    def __getitem__(self, key):
        """
            Overloaded [] operator. Gets a column based on index.

        arguments:
            key:    (int) index to a column

        retruns:
            returns the column at the index
        """
        return self.m_datacols[key]


    def __setitem__(self, key, value):
        """
            Overloaded [] operator. Sets a column based on index.

        arguments:
            key:    (int) index to a column
            value:  (list) a list of values
        """
        self.m_datacols[key] = value


    def __len__(self):
        """
            returns the number of columns

        retruns:
            the number of columns
        """
        return self.m_numcols


    def __delitem__(self, key):
        """
            Deletes the column at the key

        arguments:
            key:    (int) index to a column
        """
        del self.m_datacols[key]


    def header_to_string(self):
        """
            converts the internal list form header to a string

        returns:
            A string representing the header.
        """
        h_string = ""
        for row in self.m_header:
            for item in row:
                if item[-1:] != '\n':
                    h_string += str(item) + ','
                else:
                    h_string += str(item)
        return h_string


    #todo: sould set header here too? (srp)
    def string_to_header(self, h_str):
        """
            Converts a string to the list form header and sets the internal
        header.

        arguments:
            h_str:      (string) the string header
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


    def data_to_string(self, which = "all"):
        """
            Converts the internal data to a string

        returns:
            the data as a string
        """
        data_str = ""
        if which == "new":
            index = -1
            while (index + len(self[0]))  >= 0 and \
                  self[0][index] != self.m_last_init_date:
                temp_str = '"' + str(self[0][index]) + '"'
                for col in range(1,self.m_numcols):
                    try:
                        temp_str += ',' + ("%.2f" % self[col][index])
                    except TypeError:
                        temp_str += ',' + str(self[col][index])
                temp_str += '\n'
                data_str = temp_str + data_str
                index -= 1 
                
        elif which == "all":
            for index, date in enumerate(self.m_datacols[0]):
                data_str += '"' + str(date) + '"'
                for values in self.m_datacols[1:]:
                    try:
                        data_str += ',' + ("%.2f" % values[index])
                    except TypeError:
                        data_str += ',' + str(values[index])
                    except IndexError:
                        break
                data_str += '\n'
        else:
            raise RuntimeError, "argument <" + str(which) + "> is not supported"  
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

        returns:
            retruns colun 0
        """
        return self[0]


    def set_dates(self, new_date_col):
        """
            sets the dates column

        arguments:
            new_date_col:       ((datetime.datetime)list) the new dates
        """
        self[0] = new_date_col


    def get_header(self):
        """
            gets the header

        returns:
            The list form of the header
        """
        return self.m_header


    def set_header(self, new_header):
        """
            sets the header

        arguments:
            new_header:  (((string) list) list) the new header
        """
        self.m_header = new_header
        self.m_headlen = len(self.m_header)
        self.update_num_cols()


    def save(self, name = ""):
        """
            saves the file

        arguments:
            name:       <*.csv> (string) filename to use if internal name is
                    different
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


    #~ def append(self, name = ""):
        #~ """
            #~ will append data to the end of a file
#~ 
        #~ arguments:
            #~ name:       <*.csv> (string) filename to use if internal name is
                    #~ different
        #~ """
        #~ if name == "" :
            #~ name = self.m_name
        #~ else:
            #~ self.m_name = name
#~ 
        #~ if not os.path.exists(name):
            #~ self.save(name)
            #~ return True
#~ 
        #~ temp = CsvFile(name, True)
        #~ last_date = temp[0][-1]
        #~ 
        #~ if self[0][-1] <= last_date:
            #~ return False
        #~ index = len(temp[0])
        #~ del temp
        #~ f_stream = open (name, 'a')
        #~ w_str = ""
        #~ while (index < len(self[0])):
            #~ w_str += str(self[0][index])
            #~ col = 1
            #~ while col < self.m_numcols:
                #~ try:
                    #~ w_str += ',' + ("%.2f" % self[col][index])
                #~ except TypeError:
                    #~ w_str += ',' + str(self[col][index])
                #~ col += 1
            #~ index += 1
            #~ w_str += "\n"
        #~ f_stream.write(w_str)
#~ 
        #~ f_stream.close()
        #~ self.m_exists = True
        #~ return True


    def append(self, name = ""):
        """
            will append data to the end of a file

        arguments:
            name:       <*.csv> (string) filename to use if internal name is
                    different
                    
        returns:
            true if data is appeneded
        """
        if name == "" :
            name = self.m_name
        else:
            self.m_name = name

        if not os.path.exists(name) or \
            self.m_last_init_date == datetime.datetime(1,1,1):
            self.save(name)
            return True
        
        if self[0][-1] == self.m_last_init_date:
            return False

        f_stream = open (name, 'a')        
        f_stream.write(self.data_to_string("new"))
        f_stream.close()
        self.m_exists = True
        return True


    def exists(self):
        """
            Does the file exist?

        retruns:
            True if the file exists
        """
        return self.m_exists


    def name(self):
        """
            gets the name of the file

        Returns:
            the file name
        """
        return self.m_name


    def set_name(self, new_name):
        """
            changes the file name

        arguments:
            new_name:   <*.csv> (string) the new filename
        """
        self.m_name = new_name


    def add_dates(self, new_dates):
        """
            Adds a new date column to the file, overwrites old data.

        arguments:
            new_dates:      ((datetime.datetime)list) list of the dates
        """
        self.add_data(0, new_dates)


    def add_data(self, col, new_data):
        """
            Overwrites old data at the given column

        arguments:
            col:            (int) the column number
            new_data:       ((any type)list) list of data
        """

        self.m_datacols[col] = np.append(self.m_datacols[col], new_data)
        #print self.m_datacols[col]

