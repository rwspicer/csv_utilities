import csv_args as csva
import sys

class error_instance(object):
    def __init__(self, error, msg, other = ""):
        self.error = error
        self.msg = msg
        self.other = other
    
    def __str__(self):
        if self.other == "":
            return self.error + ": " + self.msg
        return self.error + ": " + self.msg + " (" + self.other + ")"

class error_log(object):
    
    def __init__(self):
        self.error_state = False
        self.errors = []
        
    def print_errors(self):
        if self.error_state == True:
            for item in self.errors:
                print item
        else:
            print "no errors"
    
    def get_error_state(self):
        return self.error_state
    
    def set_error_state(self, error, msg, other = ""):
        self.error_state = True
        self.errors.append(error_instance(error, msg, other))
    

error_map = {0:"clear", 1:"help", 2:"invalid flag", 3:"unknown",
             4:"missing flag"}



class utility_base(object):
    def __init__(self, title, req_flags, opt_flags, help):
        self.title = title
        self.success = "utitily has run sucessfully"
        self.errors = error_log()
        self.help = help
        self.help_bool = False
        self.commands = "unset"
        self.set_up_commands(req_flags, opt_flags)        
        

    def set_up_commands(self, r_flags, o_flags):
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
        str_len = len(msg)
        space = (size - str_len) / 2
        if (str_len % 2 == 0):
            print self.generate_rep(space, fill) + msg + \
                                                self.generate_rep(space, fill)
        else:    
            print self.generate_rep(space + 1 , fill) + msg + \
                                                self.generate_rep(space, fill)
    
    def generate_rep(self, length, fill = ' '):
        string = ""
        index = 0
        while (index < length):
            string += fill
            index += 1
        return string
    
    def check_errors(self):
        """ shcek the errors """
        pass
    
    def exit(self, ): # what is the best way to exit?
        self.print_center(" *** the utility was unsuccessful ***")

        self.print_center(" exiting ", "-")
        sys.exit(1)    
            
    def run(self): 
        self.print_center(self.title, '-')
        if self.help_bool:
            print self.help
            sys.exit(0)  
        if self.errors.get_error_state():
            self.errors.print_errors()
            self.exit()
        self.main()
        self.print_center(self.success,'-')
        
    def main(self):
        self.print_center("child classes should overwrite this")
    

