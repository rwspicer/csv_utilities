"""
csv_args.py
raswer spicer
created 2014/03/10
modified 2014/10/28

        this is a class for storing and accessing varibles and data from the
    command line
    
    version 2014.10.28.1:
        added string ify as defauld for get command value
    
    version 2014.8.1.2:
        fixed bug were help would not register as a valid flag if no flags 
    were required
    
    version 2014.8.1.1:
        added a legacy flag for old utilits that is set by default

    version 22014.7.31.1:
        updated documentation

    version 2014.3.13.1
        added documentation

"""
import sys

def strignify(value):
    """
        returns vales string represrntation
    
    pre-conditions:
        value: must have a __str__ defined
    """
    return str(value)

class ArgClass:
    """ 
    a class for reading command line arguments
    """
    def __init__(self, req_flags, opt_flags = ()
                                            , help_str = "i need some help"
                                            , legacy = True):
        """
            sets up the class and reads the arguments from the comman line

        arguments:
            req_flags:  (list) a list of flags required to be intilized
            opt_flags:  (list) optional flags
            help_str:   (string) a string to pront if "--help" key is called 
        """
        self.legacy = legacy
        self.m_flags = req_flags + opt_flags 
        self.m_help = help_str
        self.m_commands = {}
        #self.m_bad_flags = [] 
        #self.m_errors = False
        self.read_args()
        self.m_flags_not_found = []
        self.check_flags(req_flags)


    def __getitem__(self, key):
        """ 
            overloaded [] operator 
    
        argumets:
            key:    (string) a key

        returns:
            the value at key        
        """
        return self.m_commands[key]


    def __setitem__(self, key, value):
        """ 
            overloaded [] operator, this class does not allow setting of items
    
        arguments:        
            not used, but in definition because of way function is noramaly used 

        exceptions:
            RuntimeError:   if called  
        """
        raise RuntimeError, "setting flag vlaues not allowed"


    def __delitem__(self, key):
        """
        overloaded del operator, this class does not allow deleting of items

        arguments:        
            not used, but in definition because of way function is noramaly used         

        exceptions:
            RuntimeError:   if called  
        """
        raise RuntimeError, "deleting flag vlaues not allowed"


    def __len__(self):
        """ 
            overloaded length operator 

        returns:
            number of items in the command list
        """
        return len(self.m_commands)


    def read_args(self):
        """
            reads argumens from the command line based on provided flags

        exceptions:
            RuntimeError: if help string is requestes, or if a flag is not valid
        """
        cmd = []
        for index in sys.argv:
            cmd = cmd + index.split("=")
        cmd.pop(0)


        for index , item in enumerate(cmd):
            if (index % 2 == 0):
                found = False
                
                if ('--help' == item):
                    found = True
                    if self.legacy == True:
                        print self.m_help
                    raise RuntimeError, ("the help string was requested")
                
                for flags in self.m_flags:
                    if (item == flags): 

                        found = True
                        self.m_commands[flags] = cmd[index+1] 
                    
                    
                        
                if not found:
                    raise RuntimeError, (" <" + item + "> is not a valid flag ")
                    # ^^ raise an exception if any bad flag is found instead ^^
                    # self.m_errors =True
                    # self.m_bad_flags.append(item)
     


    def get_command_value(self, key , func = strignify):
        """
            gets the value that is associated with a command

        arguments:
            key:    (string) a key, one of the flags
            func:   (function) the function to get the value should take a 
                single argument
        
        returns: 
            a value
        """
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


    def keys(self):
        """
        gets a list of keys        

        returns
             a list of the flags that were used
        """
        return self.m_commands.keys()


    def check_flags(self, req_flags):
        """
        checks to see that all required flags are filled out
        if a flag is missing it is added to the flags not found list.
        
        arguments:
            req_flags:      (list)list of required flags    
        """
        for item in req_flags:
            try:
                self.m_commands[item]
            except KeyError:
                self.m_flags_not_found.append(item)
    
    def is_missing_flags(self):
        """ 
            checks for missing flags        
    
        returns: 
            true if there is a required flag misssing
        """
        return len(self.m_flags_not_found) != 0

    def get_missing_flags(self):
        """
            gets the missing flags

        returns: 
            a list of missing flags
        """
        return self.m_flags_not_found    
