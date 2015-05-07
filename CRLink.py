"""
CRLink.py
CR1000 Data Logger Interface Program
created: 2015/05/06
modified: 2015/05/07
author: rawser spicer
contact: rwspicer@alaska.edu


       This utility is for communication with a data logger. it can be 
    used for uploading and downloading programs, downloading data, and 
    viewing the general status of the data logger. It replaces the LoggerLink 
    program. 
    
    2015.05.07.1 (v1)
        first release
"""
import csv_lib.utility as util
import csv_lib.csv_file as csvf
from OCS.pakskt import pakskt, correct_table_dates 
import datetime as dt
import os
import signal


# for timing out the connection to the logger if it takes to long
def timeout (signum, frame):
    """ Function doc """
    raise StandardError, "program took too long, try again" 
    
signal.signal(signal.SIGALRM, timeout )


#~ class CRScript(object):
    #~ """ Class doc """
    #~ 
    #~ def __init__ (self, file_name):
        #~ """ Class initialiser """
        #~ self.fields = {}
        #~ script = open(file_name, 'r')
        #~ script_data = script.read().split("\n")
        #~ for row in script_data:
            #~ temp = row.split(':')
            #~ self.fields[temp[0]] = temp[1]
            #~ 
    #~ def validate (self):
        #~ """ Function doc """
        #~ pass
        
HELP = """
	   This utility is for communication with a data logger. it can be 
    used for uploading and downloading programs, downloading data, and 
    viewing the general status of the data logger. It replaces the LoggerLink 
    program. 
    
    example(retrieve a table):
      python CRLink.py --logger_id=14 --action=fetch --name=<table_name>
                       --dir=<path_to_output>
    
    example(retrieve all table):
      python CRLink.py --logger_id=14 --action=fetch+all --dir=<path_to_output>
      
    example(upload & start a program)
      python CRLink.py --logger_id=14 --action=upload --file=<program>.CR1
    
        required flags:
        
        --logger_id=<#>
                the logger id
    
        --action=<upload|download|status|fetch|fetch+all|programs|tables>
                upload: upload a program file to the logger and start it
                download: downlaod a program file from the logger
                status: returns the status of the logger.
                fetch: fetch a data table from the logger
                fetch+all: fetch all of the tables from the logger
                programs: list the programs on the logger
                tables: list the tables on the logger
        
        --optional flags:
        --host=<host IP>
                The ip adderess of the computer the logger is linked to.
                
        --port=<port number>
                The number of the port the logger is on.
                
        --filename=<filename>
                The name of the file. Use with download, upload, 
            and start.

        --name=<name>
                the name of specific table for use with fetch
                
        --directory=<directory to save output files to>
        
             
"""  
#TODO handle errors exception to error flags in utility
#TODO allow security code to be changed     
#TODO get status table
#TODO needs documentation
DEFAULT_PORT = 7808
DEFAULT_HOST = "localhost"
DEFAULT_CPU_ID = 0x802 #2050_10
class CRLink(util.utility_base):
    """ Class doc """
    
    def __init__ (self):
        """ Class initialiser """
        super(CRLink, self).__init__(" CR1000 Data Logger Interface Program " ,
                    ("--action", "--logger_id") ,
                    ("--port", "--host", "--file",
                    "--directory","--cpu_id", '--name'),
                    HELP)
        self.action = self.logger_id = self._file = self._dir = self.name = ""
        self.cpu_id = DEFAULT_CPU_ID
        self.port = DEFAULT_PORT
        self.host = DEFAULT_HOST
        self.logger = ""  
        self.action_table = {
                        "status":0,
                        "upload":1,
                        "download":2,
                        "fetch":3,
                        "programs":4,
                        "tables":5,
                        "fetch+all":6,
                        }
        
    def main (self):
        """ Function doc """
        self.get_action()
        self.evaluate_errors()
        self.get_link_info()
        self.open_link()
        self.evaluate_errors()
        print "Connection Estiblished, Processing Action"
        self.process_action()
        self.evaluate_errors()
        self.logger.close_socket()
        
    def get_opt_args (self):
        """ Function doc """
        self._file = self.commands['--file']
        temp = self.commands['--directory']
        self._dir = temp if temp != "" else "./"
        
        self.name = self.commands['--name']
        #~ print self._file, self._dir, self.name
        
    
    def get_action (self):
        """ Function doc """
        try:
            self.action = self.action_table[self.commands["--action"]]
        except KeyError:
            self.errors.set_error_state("Invalid Action", 
                                        self.commands["--action"])
                                    
    def process_action (self):
        """ Function doc """
        self.get_opt_args()
        if self.action == self.action_table['status']:
            self.action_status()
        elif self.action == self.action_table['upload']:
            if self.action_upload_program():
                self.action_start_program()
        elif self.action == self.action_table['download']:
            self.action_download_program()
        elif self.action == self.action_table['fetch']:
            self.action_save_table(self.name)
        elif self.action == self.action_table['programs']:
            self.action_list_programs()
        elif self.action == self.action_table['tables']:
            self.action_list_tables()
        elif self.action == self.action_table['fetch+all']:
            self.action_save_all()

    def action_status (self):
        """ Function doc """
        print "----loggger program status----"
        lib = self.logger.get_program_status()
        for key in lib:
            if key == 'raw':
                continue
            print key + "::" + str(lib[key]).replace('\r\n',"")
    
    def action_upload_program (self):
        """ Function doc """
        temp = self._file
        try:
            program = open(temp, 'r')
        except IOError:
            self.errors.set_error_state("I/0 Error", 
                                        "File <" + temp + "> Not Found")
            return False
        print "---- uploading program ----"
        data = program.read()
        program.close()
        
        if not self.logger.upload("CPU:"+ self.temp[temp.rfind('/')+1:], data):
            self.errors.set_error_state("Logger Error", "Program not uploaded")
            return False
        return True
        
            
    def action_start_program (self):
        """ """
        self._file = self.commands['--file'] 
        try:
            program = open(self._file, 'r')
        except IOError:
            raise IOError, "TODO: handle this error"
        print "---- starting program ----"
        self._file = '/' + self._file
        self._file = "CPU:"+ self._file[self._file.rfind('/')+1:]
        if not self.logger.start(self._file):
            raise StandardError, "TODO: handle this error"
        self._file = self._file[5:]
    
    def action_download_program (self):
        """ Function doc """
        self._file = self.commands['--file'] 
        if "" == self._file:
            raise IOError, "TODO: handle this error"
            
        print "---- downloading program ----"
        data, status = self.logger.download("CPU:"+self._file)
        if not status:
            raise StandardError, "TODO: handle this error"
        program = open(self._file, 'w')
        program.write(data)
        program.close()
        
    def action_fetch_table (self, table_name, start_rec = 0):
        """ Function doc """
        print "---- fetching table "+ table_name +"----"
        
        table, correct = \
                    correct_table_dates(self.logger.get_table_data(table_name,
                                                                   start_rec))
        if not correct:
            raise StandardError, "dates incorrect"
        
        delim = ','
        quote = lambda x: '"' + str(x) + '"'
        rows = ""
        for row in table:
            rows += quote(row['TimeOfRec']) + delim + quote(row['RecNbr'])
            for field in row['Fields']:
                rows += delim + quote(row['Fields'][field])
            rows += '\n'
            
        logger_name = "CR1000" #TODO make this a command line option
        if start_rec == 0:
            info = self.logger.get_program_status()
            line0 = '"TOA5"' + delim + '"' + logger_name + '"' + delim + \
                 quote(info["OSVer"].split('.')[0])  + delim + \
                 quote(str(info["SerialNbr"]))+ delim + \
                 quote(info["OSVer"]) + delim + \
                 quote(info["ProgName"]) + delim + \
                 quote(str(info['ProgSig'])) + delim + \
                 quote(table_name)
            
            units, intervals = self.logger.get_table_header(table_name)
            head1= '"TIMESTAMP"' + delim + '"RN"' 
            head2 = '"TS"' + delim + '"RN"'
            head3 = '""' + delim + '""'
            for key in table[0]['Fields']:#get feilds from first line
                head1 += delim + quote(key)
                head2 += delim + quote(units[key])
                head3 += delim + quote(intervals[key])
                head = line0 + '\n' + head1 + '\n' + head2 + '\n' + head3 + '\n'
            return head + rows
        else: 
            return rows
        
    def action_save_table (self, table_name):
        """ """
        if not os.path.isdir(self._dir):
            os.makedirs(self._dir)
        logger_name = "CR1000"
        file_name =  logger_name + '_' + table_name + ".dat"
        try:
            fd = open(self._dir + file_name, 'r')
            first = fd.readline()     
            fd.seek(-2, 2)            
            while fd.read(1) != "\n": 
                fd.seek(-2, 1)        
            last = fd.readline()
            start = int(last.split(',')[1].replace('"','')) + 1 
            fd.close()
        except:
            start = 0
        
        data = self.action_fetch_table(table_name, start)
        #~ print data
        fd = open(self._dir + file_name, 'a')
        fd.write(data)
        fd.close()

    def action_save_all (self):
        """ Function doc """
        for table in self.logger.tables:
            if table == "Status" or table == "Public":
                continue # TODO these tables are different
            self.action_save_table(table)
            
            
    def action_list_programs (self):
        """ Function doc """
        print "----list logger programs----"
        for programs in self.logger.programs:
            print programs
        
    def action_list_tables (self):
        """ Function doc """
        print "----list logger tables----"
        for table in self.logger.tables:
            print table
    
    def get_link_info (self):
        """ Function doc """
        self.commands.return_func = self.commands.raise_error_on_empty_str
        try:
            self.port = self.commands["--port"]
            print "Using port " + str(self.port)
        except ValueError:
            print "Using default port " + str(DEFAULT_PORT)
        self.commands.return_func = self.commands.intify
        try:
            self.host = self.commands["--host"]
            print "Using host " + str(self.host)
        except ValueError:
            print "Using default host " + str(DEFAULT_HOST)
        try :
            self.cpu_id = self.commands["--cpu_id"]
            print "Using CPU_id " + self.cpu_id 
        except ValueError:
            print "Using default CPU_id " + str(DEFAULT_CPU_ID) 
        
        self.logger_id = self.commands["--logger_id"]
        print "Using logger_id " + str(self.logger_id)
        self.commands.return_func = self.commands.stringify
    
    def open_link (self):
        """ Function doc """
        try:
            signal.alarm(10)
            self.logger = pakskt(self.host, 
                                 self.port, 
                                 30, 
                                 self.logger_id, 
                                 self.cpu_id)
            self.logger.open_socket()
            self.logger.is_reachable()
        except StandardError:
            self.errors.set_error_state("Logger is not Found", 
                                            "the logger could not be pinged")
            return
        self.logger.get_table_def()
        self.logger.get_tables()
        self.logger.get_programs()
    
    
    
if __name__ == "__main__":
    utility = CRLink()
    utility.run()
        
        
