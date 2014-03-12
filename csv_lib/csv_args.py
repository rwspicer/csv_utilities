
import sys

class ArgClass:
    def __init__(self, req_flags, opt_flags = ()
                                            , help_str = "i need some help"):
        self.m_flags = req_flags + opt_flags 
        self.m_help = help_str
        self.m_commands = {}
        #self.m_bad_flags = [] 
        #self.m_errors = False
        self.read_args()
        self.m_flags_not_found = []
        self.check_flags(req_flags)

    def __getitem__(self, key):
        return self.m_commands[key]

    def __setitem__(self, key, value):
        raise RuntimeError, "setting flag vlaues not allowed"

    def __delitem__(self, key):
        raise RuntimeError, "deleting flag vlaues not allowed"

    def __len__(self):
        return len(self.m_commands)

    def read_args(self):
        """
        reads argumens from the command line based on provided flags
        """
        cmd = []
        for index in sys.argv:
            cmd = cmd + index.split("=")
        cmd.pop(0)


        for index , item in enumerate(cmd):
            if (index % 2 == 0):
                found = False
                
                for flags in self.m_flags:
                    if (item == flags): 

                        found = True
                        self.m_commands[flags] = cmd[index+1] 
                    
                    elif ('--help' == item):
                        found = True
                        print self.m_help
                        raise RuntimeError, ("the help string was requested")
                        
                if not found:
                    raise RuntimeError, (" <" + item + "> is not a valid flag ")
                    # ^^ raise an exception if any bad flag is found instead ^^
                    # self.m_errors =True
                    # self.m_bad_flags.append(item)
     
    def get_command_value(self, key , func):
        try:
            value = self.m_commands[key]
        except KeyError:
           value = ""
        return func(value)      
    # bad flag list feature to be added ?            
    #def found_bad_flags(self):
    #    return self.m_errors
    #
    #def get_bad_flags(self):
    #    return self.m_bad_flags

    def check_flags(self, req_flags):
        """
        checks to see that all required flags are filled out
        if a flag is missing it is printed and the program exits
        
        cmds: the commands from command line
        req_flags: list of requitred flags    
        """
        for item in req_flags:
            try:
                self.m_commands[item]
            except KeyError:
                self.m_flags_not_found.append(item)
    
    def is_missing_flags(self):
        return len(self.m_flags_not_found) != 0

    def get_missing_flags(self):
        return self.m_flags_not_found    
