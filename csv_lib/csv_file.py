"""
csv_file.py
"""
import csv_lib.csv_utilities as csvu
import csv_lib.csv_date as csvd

def load_info( f_name):
    """"""
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
        if n_cols < len(segs):
            n_cols = len(segs)
    f_stream.close()
    return n_cols, h_len, header 

       

class CsvFile:
     

    def __init__(self, f_name): 
        self.m_name = f_name     
        self.m_numcols,  self.m_headlen, self.m_header = load_info(self.m_name)
        self.m_datecol = csvu.get_column(self.m_name, self.m_headlen, 0, "datetime")
        self.m_datacols = csvu.load_file_new(self.m_name, self.m_headlen, self.m_numcols)[1:]
    
    def print_file_info(self):
        print self.m_numcols
        print self.m_header
        print self.m_header
    
    def print_dates(self):
        print self.m_datecol
        print self.m_datacols

    def get_dates(self):
        return self.m_datecol

    def set_dates(self, new_date_col):
        self.m_datecol = new_date_col

    def get_header(self):
        return self.m_header        

    def set_header(self,new_header):
        self.m_header= new_header
        self.m_headlen = len(new_header)

    
    def save(self, name = ""):
        if name == "" :
            name = self.m_name
        f_stream = open (name, 'w')
            
        for rows in self.m_header:
            for cells in rows:
                if cells[-1:] != '\n':
                    f_stream.write(cells + ',')
                else:
                    f_stream.write(cells)

        for index, date in enumerate(self.m_datecol):
            f_stream.write(str(date))
            for values in self.m_datacols:
                f_stream.write(',' + str(values[index]))
            f_stream.write('\n')
        f_stream.close()



