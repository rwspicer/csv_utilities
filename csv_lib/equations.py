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
    """
        this servs as a base class for equations
    """
    def __init__(self, varible, bad_data_val = 6999):
        """ Class initialiser  """
        self.varible = varible
        self.bad_value = bad_data_val
        self.result = "not calculated"
        self.calc()
        
    def calc(self):
        print "i should be overloaded"
        
    def __float__(self):
        return self.result()


class thermistor(equation):
    def __init__(self, varible, a, b, c, offset = 0 , bad_val = 6999):
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
        self.result = (1 / (self.A + self.B * log(r) + self.C * log(r) ** 3)\
                        - 273.15) + self.offset

class poly(equation):
    """ Class doc """
    
    def __init__ (self, var, coefs, bad_val = 6999):
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
        
class flux(equation):
    """ Class doc """
    
    def __init__ (self, var, posical, negical, bad_val = 6999):
        """ Class initialiser """
        self.posical = posical
        self.negical = negical
        super(flux, self).__init__(var, bad_val)
        
                    
    def calc(self):
        """ Function doc """
        if abs(self.varible) >= 6999:
            self.result = self.bad_value
            return
        
        if self.varible >= 0:
            self.result = self.posical * self.varible
        else:
            self.result = self.negical * self.varible
        
class netrad(equation):
    """ Class doc """
    
    def __init__ (self, var, windspeed, posical, negical, bad_val = 6999):
        """ Class initialiser """
        self.posical = posical
        self.negical = negical
        self.windspeed = windspeed
        super(netrad, self).__init__(var, bad_val)
                    
    def calc(self):
        """ Function doc """
        if abs(self.varible) >= self.bad_value:
            self.result = self.bad_value
            return
            
        if(abs(self.windspeed) >= .3):
            pos_correction = 1 + (.066 * .2 * self.windspeed)/ \
                                (.066 + (.2 * self.windspped))
            neg_correction = (.00174 * self.windspeed) + .99755
            uncorrected = flux(self.varible, self.posical, self.negical,
                                             self.badvalue).result
            if uncorrected >= 0:
                self.result = uncorrecte * pos_correction
            else:
                self.result = uncorrecte * neg_correction
        else:
            self.result = flux(self.varible, self.posical, self.negical,
                                             self.badvalue).result

class rt_sensor(equation):
    """ Class doc """
    
    def __init__ (self, var, div, offset, mult, bad_val = 6999):
        """ Class initialiser """
        self.div = div
        self.ofset = offset
        self.mult = mult 
        super(rt_sensor, self).__init__(var, bas_val)
        
                    
    def calc(self):
        """ Function doc """
        if abs(self.varible) >= 6999:
            self.result = self.bad_value
            return
    
        self.result = ((self.varible / self.div) + self.offset) / self.mult
