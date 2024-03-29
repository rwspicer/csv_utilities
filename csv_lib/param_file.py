"""
param_file.py
rawser spicer
created: 2014/08/22
modified: 2014/12/04

Part of DataPro Version 3

    this file presnts classes that represent a param file
    
    version 2014.12.04.1:
        updated error to give right line #
    
    version 2014.11.25.1:
        updated exception errors

    version 2014.9.8.4:
        fixed "output_header" keys
 
    version 2014.9.8.3:
        added "d_element" key to dictionary

    version 2014.9.8.2:
        fixed issue with extra '\r' newline characters 

    version 2014.9.8.1:
        fixed issue with extra '"' characters 

"""

class Param(object):
    """
    this class represnts a single data point in the param file 
    """
    
    def __init__(self , d_elem, d_type, i_pos, 
            c1, c2, c3, c4, c5, c6, c7, qch, qcl, qcs,
            oh_name ,oh_units, oh_meas):
        """
            initlization functions sets interanl data
        
        arguments:
            d_elem:     (string) name of the data element
            d_type:     (string) its data type
            i_pos:      (string) array input position
            c1:         (string) coefficient 1
            c2:         (string) coefficient 2
            c3:         (string) coefficient 3
            c4:         (string) coefficient 4
            c5:         (string) coefficient 5
            c6:         (string) coefficient 6
            c7:         (string) coefficient 7
            qch:        (string) quality control param high
            qcl:        (string) quality control param low
            qcs:        (string) quality control stepS
            oh_name:    (string) output header name
            oh_units:   (string) output header units
            oh_meas:    (string) output header measurment
        """
        self.element = d_elem
        self.d_type = d_type
        self.input_pos = i_pos
        self.coefs = (c1, c2, c3, c4, c5, c6, c7)
        self.Qc_high = qch
        self.Qc_low = qcl
        self.Qc_step = qcs
        self.out_name = oh_name
        self.out_units = oh_units
        self.out_measurement = oh_meas
        
    def __getitem__(self, key):
        """
            overlaods __getitem__ operator
            
        arguments:
            key:    (string) should be one of the vaild names prented below
            
        returns:
            the data associated with the key
        """
        if key == "d_element":
            return self.element
        if key == "Data_Type":
            return self.d_type
        if key == "Input_Array_Pos":
            return self.input_pos
        if key == "Coef_1":
            return self.coefs[0]
        if key == "Coef_2":
            return self.coefs[1]
        if key == "Coef_3":
            return self.coefs[2]
        if key == "Coef_4":
            return self.coefs[3]
        if key == "Coef_5":
            return self.coefs[4]
        if key == "Coef_6":
            return self.coefs[5]
        if key == "Coef_7":
            return self.coefs[6]
        if key == "Qc_Param_High":
            return self.Qc_high
        if key == "Qc_Param_Low":
            return self.Qc_low
        if key == "Qc_Param_Step":
            return self.Qc_step
        if key == "Output_Header_Line_2" or key == "Output_Header_Name":
            return self.out_name
        if key == "Output_Header_Line_3" or key == "Output_Header_Units":
            return self.out_units
        if key == "Output_Header_Line_4" or \
                                key == "Output_Header_Measurment_Type":
            return self.out_measurement         
    
    def __str__(self):
        """
        retruns:
            a string of the data
        """
        return str(vars(self))

class ParamFile(object):
    """
        this class loads and represents a param file
    """
    def __init__(self, file_name):
        """
            sets up the class
        
        arguments:
            file_name:      (string) the name of the file
        """
        self.params = []
        self.file_name = file_name
        self.read_file()
        #print self.params[1]
     
    def read_file(self):
        """
            reads the file
        """
        try:
            p_file = open(self.file_name, "r") 
        except ( IOError ):
            raise IOError
        p_file.readline()
        idx = 1
        for rows in p_file.read().strip().replace('"',""). \
                                                replace("\r","").split('\n'):
            idx += 1
            args = rows.split(',')
            try:
                self.params.append(Param(args[0], args[1], args[2], 
                                     args[3], args[4], args[5], 
                                     args[6], args[7], args[8], 
                                     args[9], args[10], args[11], 
                                     args[12], args[13], args[14], 
                                     args[15]))
            except ( IndexError ):
                raise IOError
                 
        p_file.close()
           
        
