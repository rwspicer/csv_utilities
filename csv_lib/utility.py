"""
utility.py
Rawser Spicer
created: 2014/08/01
modified: 2014/09/08

        this fill contains classes to help implement a base utility class. The 
    class should be used as a base class for new utilities. The class will hadle
    the internal runnings of a utility

    version 2014.9.8.1:
        added evaluate_error to handle error checking and and reduce code 
    dupilcation during error check phase 

    version 2014.8.5.1:
        Basic version of the utility_base class, and error classes. A utility 
    that inherites from utility_base can now have access to the command 
    line arguments and errors.     

"""
import csv_args as csva
import sys

class error_instance(object):
    """
        this class is the represntation of a singal error 
    """
    def __init__(self, error, msg, other = ""):
        """
            initilizes the error
            
        arguments: 
            error:      (string) the errors name
            msg:        (string) decription of the error
            other:      (stirng) any other info about error
        """
        self.error = error
        self.msg = msg
        self.other = other
    
    def __str__(self):
        """
            converts the error to a sting
    
        returns:
            a string 
        """
        if self.other == "":
            return self.error + ": " + self.msg
        return self.error + ": " + self.msg + " (" + self.other + ")"



class error_log(object):
    """
        this class represents a log of all errors that occur
    """    
    def __init__(self):
        """
            initilzes the error log to be free of errors
        """    
        self.error_state = False
        self.errors = []
        
    def print_errors(self):
        """
            prints the errors
        """
        if self.error_state == True:
            for item in self.errors:
                print item
        else:
            print "no errors"
    
    def get_error_state(self):
        """
            gets the error state
        
        returns:
            true if there is an error
        """
        return self.error_state
    
    def set_error_state(self, error, msg, other = ""):
        """
            set an error by adding it to the log and seting error state to true
        
        arguments:
            error:      (string) the error
            msg:        (string) a description of the error
            error:      (string) other info about the error
        """
        self.error_state = True
        self.errors.append(error_instance(error, msg, other))
        


class utility_base(object):
    """
        Base class for utilities. Derived classes should over write main()
    """
    def __init__(self, title, req_flags, opt_flags, help):
        """
            initlizes the utility
            
        arguments:
            title:      (string) the utilities title
            req_flags:  ((string) list) a list of required flags
            opt_flags:  ((string) list) a list of optional flags
            help:       (string) the help information
        """
        self.title = title
        self.success = "utitily has run sucessfully"
        self.errors = error_log()
        self.help = help
        self.help_bool = False
        self.commands = "unset"
        self.set_up_commands(req_flags, opt_flags)        
        
    def set_up_commands(self, r_flags, o_flags):
        """
            this function sets up the command argumets for use by the utility
        
        arguments:
            r_flags:  ((string) list) a list of required flags
            o_flags:  ((string) list) a list of optional flags
        """
        try:
            self.commands = csva.ArgClass(r_flags, o_flags, self.help, False)
        except RuntimeError, (error_message):
            if str(error_message) == "the help string was requested":
                self.help_bool = True
            elif str(error_message)[:2] == " <":
                self.errors.set_error_state("invalid flag", 
                                            "a set flag is not recognized",
                             str(error_message)[2:str(error_message).find(">")])
            else:
                self.errors.set_error_state("unknown", "unknown")
            return
                
        if self.commands.is_missing_flags():
            for item in self.commands.get_missing_flags():
                self.errors.set_error_state("missing flag", 
                                            "a required flag is unset",
                                            item)
                               
    def print_center(self, msg, fill=' ', size=80):
        """
            prints the message in the center of a terminal
        
        arguments:
            msg:        (string) the message
            fill:       (char) fills the empty space
            size        (int) size of the terminal
        """
        str_len = len(msg)
        space = (size - str_len) / 2
        if (str_len % 2 == 0):
            print self.generate_rep(space, fill) + msg + \
                                                self.generate_rep(space, fill)
        else:    
            print self.generate_rep(space + 1 , fill) + msg + \
                                                self.generate_rep(space, fill)
    
    def generate_rep(self, length, fill = ' '):
        """
            generates a string of a char at the given length
            
        arguments:
            length:     (int) the lenght of the string
            fill:       (char) the character to write
            
        returns:
            a string 
        """
        string = ""
        index = 0
        while (index < length):
            string += fill
            index += 1
        return string
    
    def exit(self):
        """
            exits the utility
        """
        self.print_center("*** the utility was unsuccessful ***")

        self.print_center(" exiting ", "-")
        sys.exit(1)   
            
    def run(self): 
        """
            runs the utility
        """
        self.print_center(self.title, '-')
        if self.help_bool:
            print self.help
            sys.exit(0)  
        self.evaluate_errors()
        #~ if self.errors.get_error_state():
            #~ self.errors.print_errors()
            #~ self.exit()
        self.main()
        self.print_center(self.success,'-')
        
    def main(self):
        """
            the body of the utility. should be overwritten
        """
        self.print_center("child classes should overwrite this")
    
    def evaluate_errors(self):
        """
            checks the error state and exits
        """
        if self.errors.get_error_state():
            self.errors.print_errors()
            self.exit()
