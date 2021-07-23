"""
utility.py
Rawser Spicer
created: 2014/08/01
modified: 2014/09/03

        this fill contains classes to help implement a base utility class. The
    class should be used as a base class for new utilities. The class will hadle
    the internal runnings of a utility

    v. 2015.9.3.1:
        bug fix for utilities not run with active terminal

    v. 2015.6.26.1:
        updated the print center function to change with the window size

    version 2014.11.05.2:
        fixed typo in exit messege

    version 2014.11.05.1:
        updated dummy main function

    version 2014.10.29.1:
        refromated error messeges

    version 2014.10.22.1:
        added feature to time main utilities main function

    version 2014.10.20.1:
        updated error messages

    version 2014.9.8.1:
        added evaluate_error to handle error checking and and reduce code
    dupilcation during error check phase

    version 2014.8.5.1:
        Basic version of the utility_base class, and error classes. A utility
    that inherites from utility_base can now have access to the command
    line arguments and errors.

"""
from __future__ import absolute_import
from __future__ import print_function
import csv_lib.csv_args as csva
import sys
import datetime as dt
from csv_lib.csv_file import CsvFile #for saving timing

class error_instance(object):
    """
        this class is the represntation of a single error
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
        tab = "        "
        tmp_msg = str(self.error ) + ": " +  self.msg
        if len(tmp_msg) > 80:
            tmp_msg = self.error +":\n"
            temp = tab+self.msg
            while True:
                if len(temp) > 80:
                    idx = temp[:80].rfind(" ")
                    half1 = temp[:idx]
                    temp = tab+ temp[idx:].lstrip()
                    tmp_msg += half1 + '\n'
                else:
                    tmp_msg += temp
                    break
        if self.other == "":
            return tmp_msg
        return tmp_msg + "\n\t(" + self.other + ")" \
                + " [try <--help> for info on running utility]"



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
                print ( item )
        else:
            print ( "no errors" )

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
    def __init__(self, title, req_flags, opt_flags, help_str):
        """
            initlizes the utility

        arguments:
            title:      (string) the utilities title
            req_flags:  ((string) list) a list of required flags
            opt_flags:  ((string) list) a list of optional flags
            help_str:       (string) the help information
        """
        self.title = title
        self.success = "utility has run successfully"
        self.errors = error_log()
        self.help_str = help_str
        self.help_bool = False
        self.commands = "unset"
        # --- timing features --- v2014.10.22.1
        self.timing_bool = False
        self.timing_path = ""
        self.start_time = "usnet"
        self.runtime = "unset"
        # ------------------------
        self.set_up_commands(req_flags, opt_flags)

    def set_up_commands(self, r_flags, o_flags):
        """
            this function sets up the command argumets for use by the utility

        arguments:
            r_flags:  ((string) list) a list of required flags
            o_flags:  ((string) list) a list of optional flags
        """
        try:
            self.commands = csva.ArgClass(r_flags, o_flags, self.help_str, False)
        #except (RuntimeError, error_message):
        except Exception as error_message :
            if str(error_message) == "the help string was requested":
                self.help_bool = True
            elif str(error_message)[:2] == " <":
                self.errors.set_error_state("INVALID FLAG:",
                        "The utility does not support a given flag.",
        "FLAG: " + str(error_message)[2:str(error_message).find(">")])
            else:
                self.errors.set_error_state( error=error_message , msg="unknown")
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
        import fcntl, termios, struct
        try:
            size = struct.unpack('HHHH', fcntl.ioctl(0, termios.TIOCGWINSZ,
                                            struct.pack('HHHH', 0, 0, 0, 0)))[1]
        except ( IOError ):
            size = 80

        space = (size - str_len) / 2
        #~ print size, str_len, space
        if (str_len % 2 == 1) and (size % 2 == 0):
            print((self.generate_rep(space + 1, fill) + msg + \
                                                self.generate_rep(space, fill) ))
        elif (str_len % 2 == 0) and (size % 2 == 1):
            print(( self.generate_rep(space + 1, fill) + msg + \
                                                self.generate_rep(space , fill) ))
        else:
            print(( self.generate_rep(space, fill) + msg + \
                                                self.generate_rep(space , fill) ))

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
            print(( self.help_str ))
            self.print_center(" Help has been displayed, exiting ",'-')
            sys.exit(0)
        self.evaluate_errors()

        # --- timing features --- v2014.10.22.1
        if self.timing_bool == True:
            self.start_time = dt.datetime.now()
            self.main()
            self.runtime = dt.datetime.now() - self.start_time
            self.save_timing()
        # -----------------------
        else:
            self.main()
        self.print_center(self.success,'-')

    def main(self):
        """
            the body of the utility. should be overwritten
        """
        self.print_center("This is an example main function, & ")
        self.print_center("child classes should overwrite this.")

    def evaluate_errors(self):
        """
            checks the error state and exits
        """
        if self.errors.get_error_state():
            self.errors.print_errors()
            self.exit()

    def save_timing(self):
        """
        this functions save the timing to a specified output file

        pre-conditions:
            self.timing_path:       (string) a filename/path; cannot be ""
        """
        if self.timing_path == "":
            return
        timing_file = CsvFile(self.timing_path, opti = True)
        if not timing_file.exists():
            timing_file.set_header([["Utility Runtime Log", self.title + "\n"],
                                    ["timestamp", "runtime\n,seconds\nDate,Tot\n"]])
        timing_file.add_dates(self.start_time.replace(microsecond=0))
        timing_file.add_data(1,self.runtime.total_seconds())
        timing_file.append()





