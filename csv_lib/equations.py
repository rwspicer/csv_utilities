"""
equations.py
rawser spicer
created: 2014/08/28
modified: 2014/09/29

Part of DataPro Version 3

    this file presnts classes that are used as equation functions by data pro

    version 2014.9.4.1:
        updated documentation and each class now allows any type converable to
    float to be passed as an argument to variable

    version 2014.9.29.1:
        fixed minor errors
"""
from math import log


class   equation(object):
    """
        this servs as a base class for equations
    """
    def __init__(self, variable, bad_data_val = 6999):
        """
        Class initializer

        arguments:
           variable:        (convertible to float) the resistance variable value
           bad_val         (convertible to int) the value to indicate a
                        bad data item
        """
        self.variable = float(variable)
        self.bad_value = int(bad_data_val)
        self.bad_val = int(bad_data_val)
        self.result = "not calculated"
        self.calc()

    def calc(self):
        """
            Placeholder calc function. This function should be overloaded to
        calcualte the result of the function being represnted.
        """
        print "i should be overloaded"

    def __float__(self):
        """
            Overloads the float type converter to return the result of the
        calculation.
        """
        return self.result


class thermistor(equation):
    """
        This class is for processing thermistor values using the
    Steinhart-Hart equation. This class takes a resistance and cofficents and
    calculates a temperature into the resulat variable
    """
    def __init__(self, variable, a, b, c, offset = 0.0 , bad_val = 6999):
        """
        Class initializer

        arguments:
            variable:        (convertible to float) the resistance variable value
            a, b, c:        (convertible to float) the Stienhart-Hart
                        coefficents
            offset:         (convertible to float) a correctional offset
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        self.A = float(a)
        self.B = float(b)
        self.C = float(c)
        try:
            self.offset = float(offset)
        except:
            self.offset = 0.0
        super(thermistor, self).__init__(variable, bad_val)


    def calc(self):
        """
        Calculates the Steinhart-Hart conversion from resastanc to temperature
        """
        if abs(self.variable) >= 6999 or self.variable <=0:
            self.result = self.bad_value
            return
        r = self.variable * 1000
        self.result =   1 / ( self.A + (self.B * log(r)) + self.C *( ( log(r) * log(r) * log(r) )) )    + self.offset - 273.15

class mrctherm(equation):
    """
        This class is for processing thermistor values using the
    Steinhart-Hart equation. This class takes a resistance and cofficents and
    calculates a temperature into the resultant variable
    """
    def __init__(self, variable, mrcexcite, offset = 0,  bad_val = 6999):
        """
        Class initializer

        arguments:
            variable:        (convertible to float) the resistance variable value
            offset:         (convertible to float) a correctional offset
            mrcexccol:         column for the mrc excitation voltage
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        self.mrcexcite = float(mrcexcite)
        self.variable = float(variable)
        self.A = 2.4886e-3
        self.B = 2.5079e-4
        self.C = 3.1754e-7
        self.offset = float(offset)
        super(mrctherm, self).__init__(variable, bad_val)


    def calc(self):
        """
        Calculates the Steinhart-Hart conversion from millivolt output on the logger into temperature

        """

        if abs(self.variable) >= 6999 or self.variable <=0:
            self.result = self.bad_value
            return

        mrcv0 = self.variable
        mrcex = self.mrcexcite

        r = ( (mrcex - mrcv0)  / mrcv0)  * 20
        self.result = (1 / (( self.A + self.B * log(r) + self.C * ( log(r) ** 3) ) ) \
                        - 273.15) + self.offset

class poly(equation):
    """
        This class represents a polynomial function with a variable number of
    terms. The coefficient for each term should be passed in a tuple containing
    the coefficients value at the power term it will be used at.
    (ie. 4x^2 + 1 is (1 , 0, 4), or 5x^3 is (0, 0, 0, 5)
    """

    def __init__ (self, var, coefs, bad_val = 6999):
        """
        Class initializer

        Arguments:
            var:            (convertible to float)  the domain value
            coefs:          (tuple of numbers) the cofficents for the polynomial
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        self.coefs = coefs
        super(poly, self).__init__(var, bad_val)

    def calc(self):
        """
        Calculates the polynomial function value
        """
        if abs(self.variable) >= 6999:
            self.result = self.bad_value
            return

        temp = 0
        for idx in range(len(self.coefs)):
            temp += float(self.coefs[idx]) * self.variable ** idx
        self.result = temp

class sm(equation):
    """
        This class represents a polynomial function multiplied by 100% with a variable number of
    terms. The coefficient for each term should be passed in a tuple containing
    the coefficients value at the power term it will be used at.
    (ie. 4x^2 + 1 is (1 , 0, 4), or 5x^3 is (0, 0, 0, 5)
    """

    def __init__ (self, var, coefs, bad_val = 6999):
        """
        Class initializer

        Arguments:
            var:            (convertible to float)  the domain value
            coefs:          (tuple of numbers) the cofficents for the polynomial
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        self.coefs = coefs
        super(sm, self).__init__(var, bad_val)

    def calc(self):
        """
        Calculates the polynomial function value
        """
        if abs(self.variable) >= 6999:
            self.result = self.bad_value
            return

        temp = 0
        for idx in range(len(self.coefs)):
            temp += float(self.coefs[idx]) * self.variable ** idx
        self.result = temp * 100
        if abs(self.result) <0:
            self.result = self.bad_value
            return

class flux(equation):
    """
    The function this class reprsents calculats a flux value
    """

    def __init__ (self, var, posical, negical, bad_val = 6999):
        """
        Class initializer

        Arguments:
            var:            (convertible to float)  the domain value
            posical:        (convertible to float) the multiplier for positive
                        values
            negical:        (convertible to float) the multiplier for negative
                        values
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        self.posical = float(posical)
        self.negical = float(negical)
        super(flux, self).__init__(var, bad_val)


    def calc(self):
        """
        calculates the flux into the result member
        """
        if abs(self.variable) >= 6999:
            self.result = self.bad_value
            return

        if self.variable >= 0:
            self.result = self.posical * self.variable
        else:
            self.result = self.negical * self.variable

class netrad(equation):
    """
    This class represents a netrad function
    """

    def __init__ (self, var, windspeed, posical, negical, bad_val = 6999):
        """
        Class initializer

        Arguments:
            var:            (convertible to float)  the domain value
            windspeed:      (convertible to float)
            posical:        (convertible to float) the multiplier for positive
                        values
            negical:        (convertible to float) the multiplier for negative
                        values
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        self.posical = float(posical)
        self.negical = float(negical)
        self.windspeed = float(windspeed)
        super(netrad, self).__init__(var, bad_val)

    def calc(self):
        """
        calculates the netrad in to the result memver
        """

        if abs(self.variable) >= self.bad_val :
            self.result = self.bad_val
            return

        if(abs(self.windspeed) >= .3):
            pos_correction = 1 + (.066 * .2 * self.windspeed)/ \
                                (.066 + (.2 * self.windspeed))
            neg_correction = (.00174 * self.windspeed) + .99755
            uncorrected = flux(self.variable, self.posical, self.negical,
                                             self.bad_val).result
            if uncorrected >= 0:
                self.result = uncorrected * pos_correction
            else:
                self.result = uncorrected * neg_correction
        else:
            self.result = flux(self.variable, self.posical, self.negical,
                                             self.bad_val).result




class rt_sensor(equation):
    """
        This class represnts a sensor calibration given by the function
    processed value = ( ( data_element / val_a ) + val_b ) / val_c
    """

    def __init__ (self, var, div, offset, mult, bad_val = 6999):
        """
        Class initializer

        Arguments:
            var:            (convertible to float) the domain value
            div:            (convertible to float) a divisor
            offset:         (convertible to float) an offset
            mult:           (convertible to float) a multiplier
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        self.div = float(div)
        self.offset = float(offset)
        self.mult = float(mult)
        super(rt_sensor, self).__init__(var, bad_val)


    def calc(self):
        """
        calculates the calibration
        """
        if abs(self.variable) >= 6999:
            self.result = self.bad_value
            return

        self.result = ((self.variable / self.div) + self.offset) / self.mult


class rh(equation):
    """
        This class corrects relative humidity data to 100% during highly saturated conditions.
    """

    def __init__ (self, var, bad_val = 6999):
        """
        Class initializer

        Arguments:
            var:            (convertible to float)  the domain value
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        super(rh, self).__init__(var, bad_val)

    def calc(self):
        """
        Calculates the polynomial function value
        """
        if abs(self.variable) >= 108:
            self.result = self.bad_value
            return
        elif self.variable > 100 and self.variable < 108 :
            self.result = 100
            return
        self.result = self.variable

class sw(equation):
    """
        This class corrects shortwave radiation data to 0 at night when it just a bit below 0 and should read 0.
    """

    def __init__ (self, var, bad_val = 6999, mult = 1.0):
        """
        Class initializer

        Arguments:
            var:            (convertible to float)  the domain value
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        if float(mult) == 0 : 
            self.mult = 1.0
        else:
            self.mult = float(mult)
        super(sw, self).__init__(var, bad_val)

    def calc(self):
        """
        Calculates the polynomial function value
        """
        rawval = self.variable
        adjustedval = rawval * self.mult
        if abs(self.variable) >= 6999:
            self.result = self.bad_value
            return
        elif adjustedval < 0.0 and adjustedval > -40.0 :
            self.result = 0
            return
        self.result = adjustedval

class battery(equation):
    """
        This class looks for out of range battery voltage values... usually a symptom of a data logger problem or a misclassified data element.
    """

    def __init__ (self, var, bad_val = 6999):
        """
        Class initializer

        Arguments:
            var:            (convertible to float)  the domain value
            bad_val:        (convertible to int) the value to indicate a
                        bad data item
        """
        super(battery, self).__init__(var, bad_val)

    def calc(self):
        """
        Calculates the polynomial function value
        """
        if abs(self.variable) >= 20.0:
            self.result = self.bad_value
            return
        elif self.variable < 8.0 :
            self.result = self.bad_value
            return
        self.result = self.variable



