"""
key_file.py
rawser spicer
created: 2014/08/25
modified: 2014/11/14

Part of DataPro Version 3

    this file presnts classes that represent a key file as a dictionary
    
    version 2014.11.14.1
        extra trailing whitespace will be removed from values
    
    version 2014.9.16.1
        extra leading whitespace will be removed from values
"""

class KeyFile(object):
    """
        class represntation of a key file
    """
    def __init__(self, file_name):
        """
            initlizes the key file dictionary
            
        arguments:
            file_name:      (string) the file name
        """
        k_file = open(file_name,"r")
        k_text = k_file.read()
        k_file.close()
        self.lib = {}
        self.name = '?'
        for line in k_text.split("\n"):
            if line == "":
                continue
            if line[0] == '[':
                self.name = line[1:-1]
                continue
            if line[0] == '#':
                continue
            self.lib[line.split(' = ')[0]] = line.split(' = ')[1].strip(" ")
            
    def __getitem__(self, key):
        """
            overloads __getitem__ function
        
        arguments:
            key:    (string) a key
        
        returns:
            the keys value
        """
        return self.lib[key]
        
