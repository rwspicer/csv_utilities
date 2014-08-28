"""
equations.py
rawser spicer
created: 2014/08/28
modified: 2014/08/28

Part of DataPro Version 3

    this file presnts classes that are used as equation functions by data pro
"""
from math import log


class   equation(object):
    def __init__(self, varible, bad_data_val = 6999):
        """ Function doc """
        self.varible = varible
        self.bad_value = bad_data_val
        self.result = "not calculated"
        self.calc()
        
    def calc(self):
        print "i should be overloaded"
        
    def __float__(self):
        return self.result()


class thermistor(equation):
    def __init__(self, varible, a, b, c, offset, bad_val):
        """ Function doc """
        self.A = a
        self.B = b
        self.C = c
        self.offset = offset
        super(thermistor, self).__init__(varible, bad_val)
        
    
    def calc(self):
        if abs(self.varible) >= 6999 or self.varible <=0:
            self.result = self.bad_value
            return
        
        r = self.varible * 1000
        self.result = (1 / (self.A + self.B * log(r) + self.C * log(r) ** 3)/ 
                        - 273.15) + self.offset

class poly(equation):
    """ Class doc """
    
    def __init__ (self, var, coefs, bad_val):
        """ Class initialiser """
        self.coefs = coefs
        super(poly, self).__init__(var, bad_val)
        
    def calc(self):
        """ Function doc """
        if abs(self.varible) >= 6999:
            self.result = self.bad_value
            return
        
        temp = 0 
        for idx in range(len(self.coefs)):
            temp += self.coefs[idx] * self.varible ** idx
        self.result = temp
        
                    
