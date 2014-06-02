"""
LoggerLink.py 
Rawser Spicer -- rwspicer@alaska.edu
Created: 2014/05/23
modified: 2014/06/02

        this appilcation and class are used for communicating with the 
    cr1000 datalogers. the commuincation wiht the logger uses the pakbus 
    package avaible at http://sourceforge.net/projects/pypak/files/ 
    
    version 2014.6.2.1:
        fixed the issue where olny first part of data table from logger 
    was written to .dat file. Added feature to collect olny new if a 
    .dat file alread exists.
        
    
    version 2014.5.30.1: 
        fixed the issue where the date on the data from logger was 20 
    years off

    version 2014.5.29.2: 
        the write function has been completed and can wite a table to a
    . dat file. 
    
    version 2014.5.29.1:
        most features work and commets have been added to the top of the
    file. the downloading and saving of data from logger is still a work
    in progress.
    

"""
import csv_lib.csv_args as csva
from csv_lib.csv_utilities import print_center, exit_on_success, exit_on_failure
import pakbus
import datetime as dt


UTILITY_TITLE = " data logger communicator "

OPT_FLAGS = ("--action", "--port", "--host", "--filename", 
             "--tablename")
REQ_FLAGS = ()

HELP_STRING = """
        This utility is for communication with a datalogger. it can be 
    used for uploading and downloading programs, downloading data, and 
    veiwing the general status of the datalogger. 
              """

class LoggerLink(object):
    """ this class represents a connection to the data logger """
    
    def __init__(self, host = 'localhost', port = 7809, timeout = 30, 
                            logger_id = 0x001, computer_id = 0x802 ):
        """ this initilizer function sets up the connection """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.l_id = logger_id
        self.c_id = computer_id
        self.link = pakbus.open_socket(self.host, self.port
                                                 , self.timeout)
        self.ping()
        self.progs = []
        self.table_list = []
        FileData, Response = pakbus.fileupload(self.link, self.l_id, self.c_id, '.TDF')
        self.tabledef = pakbus.parse_tabledef(FileData)
        
        self.fetchprogs()
        
    def set_host(self, val):
        """ set the host"""
        self.host = val
        
    def set_port(self, val):
        """ set the port"""
        self.port = val
                                        
    def relink(self):
        """reestiblish the link with the data logger"""
        self.link = pakbus.open_socket(self.host, self.port
                                                 , self.timeout)
                                                 
    def ping(self):
        """pings the logger"""
        rsp = {}
        while rsp == {}:
            rsp = pakbus.ping_node(self.link, self.l_id, self.c_id)
        return rsp
        
    def upload(self, filename, s_cond = 0x0000, swath = 0x0200):
        """ upload a file to the logger"""
        self.ping()
        f = open(filename, 'rb')
        f_contents = f.read()
        f.close()
        rsp = pakbus.filedownload(self.link, self.l_id, self.c_id, 
                            "CPU:"+filename, f_contents , s_cond, swath)
        self.fetchprogs()
        return rsp
        
                            
    def download(self, filename, s_cond = 0x0000):
        """ download a file from the loger """
        self.ping()
        filedata, response = pakbus.fileupload(self.link, self.l_id, self.c_id, 
                                        "CPU:"+filename ,s_cond)
                                        
        if response != 13:
            return response 
        f = open(filename,'w')
        print filedata
        f.write(filedata)
        f.close()
        return response
                            
    def unlink(self):
        """ close the link to the data logger"""
        pakbus.send(self.link, pakbus.pkt_bye_cmd(self.l_id, self.c_id))
        self.link.close()

    def info(self):
        """ print the info for the link """
        return "host = " + str(self.host) + '\n' + \
               "port = " + str(self.port) + '\n' + \
               "timeout = " + str(self.timeout) + '\n' + \
               "logger ID = " + str(self.l_id) + '\n' + \
               "computer ID = " + str(self.c_id) 
        
    def progstat(self):
        """ return the status of the running program"""
        self.ping()
        pkt, TranNbr = pakbus.pkt_getprogstat_cmd(self.l_id, self.c_id)
        pakbus.send(self.link, pkt)
        hdr, msg = pakbus.wait_pkt(self.link, self.l_id, self.c_id, TranNbr)
        return msg
        
    def progstart(self, FileName):
        """starts the given progam"""
        self.ping()
        return self.progctrl(FileName,1)    
               
    def progctrl(self, FileName, FileCmd, SecurityCode = 0x0000, TranNbr = None):
        """ allows for commands to be sent to the data logger to controll the program
            FileCmd - 0 turns off program (ithink),  1 starts a program(probably might be 2) 
        """
        pkt, t = pakbus.pkt_filecontrol_cmd(self.l_id, self.c_id,  FileName, 
                            FileCmd, SecurityCode, TranNbr)
        pakbus.send(self.link, pkt)
        hdr, msg = pakbus.wait_pkt(self.link,self.l_id, self.c_id, TranNbr)
        
        return msg
        
    def fetchprogs(self):
        """ makes a list of the programs avaible on the data logger"""
        FileData, Response = pakbus.fileupload(self.link, self.l_id, self.c_id, '.DIR')
        file_dir = pakbus.parse_filedir(FileData)
        for files in file_dir['files']:
            self.progs.append(files['FileName'])
            
    def listprogs(self):
        """ lsit programs on the logger"""
        return self.progs
        
    def refresh_tabledef(self):
        self.ping()
        FileData, Response = pakbus.fileupload(self.link, self.l_id, self.c_id, '.TDF')
        self.tabledef = pakbus.parse_tabledef(FileData)
        
    def listtables(self, refresh = False):
        """ list the tables """
        if (self.table_list == []) or refresh:
            self.ping()
            self.table_list = []
            for table in self.tabledef:
                self.table_list.append(table['Header']['TableName'])
        return self.table_list
        
    def fetchdata(self, t_name = "Snow", lastrecs = 0):
        """step 1 ping fetch the data form a given table"""
        self.ping()
        array = [] 
        
        try:
            recs, more =  pakbus.collect_data(self.link, self.l_id, self.c_id, self.tabledef, t_name,P1 = 1)
        except StandardError:
            print "Error: table " + t_name + " was not found."
        numRecs = recs[0]['RecFrag'][0]['RecNbr']  +1
        
        if lastrecs != 0:
            numRecs -= (lastrecs + 1)
        #~ print numRecs
        more = 1 
        while numRecs != 0:
            recs, more =  pakbus.collect_data(self.link, self.l_id, self.c_id, self.tabledef, t_name,P1 = numRecs)
            if len(recs) < 1 :
                return array
            for items in recs[0]['RecFrag']:
                array.append(items)
            temp = recs[0]['NbrOfRecs'] 
            #~ print temp
            numRecs -= temp 
            #~ print numRecs
            
        return array
        
    def get_unit_info(self, t_name):
        """ gets the units for the table """
        #~ self.ping()
        tableno = pakbus.get_TableNbr(self.tabledef, t_name) - 1
        
        units = {}
        processing = {}
        fields = self.tabledef[tableno]['Fields']
        for items in fields:
            units[items['FieldName']] = items['Units']
            processing[items['FieldName']] = items['Processing']
        return units, processing 
        
        
    def write(self, table, logger_name, delim = ','):
        """ writes given table to the given file name """
        filename = logger_name + '_' + table + ".dat"
        try:
            f = open(filename, 'r')
            first = f.readline()     
            f.seek(-2, 2)            
            while f.read(1) != "\n": 
                f.seek(-2, 1)        
            last = f.readline()
            oldrecs = int(last.split(',')[1].replace('"',''))
            f.close()
            f_exists = True
        except IOError:
            oldrecs = 0
            f_exists = False
            
        data = self.fetchdata(table, oldrecs)
        
        if len(data) == 0:
            return "no data to write"
        info = self.progstat()
        units, pro = self.get_unit_info(table)
        line1 = '"TOA5"' + delim + '"' + logger_name + '"' + delim + \
                 '"' + info["OSVer"].split('.')[0]  + '"' + delim + \
                 '"' + str(info["SerialNbr"]) + '"' + delim + \
                 '"' + info["OSVer"] + '"' + delim + \
                 '"' + info["ProgName"] + '"' + delim + \
                 '"' + str(info['ProgSig']) + '"' + delim + \
                 '"' + table + '"\n'
        line2 = '"TIMESTAMP"' + delim + '"RN"' 
        line3 = '"TS"' + delim + '"RN"'
        line4 = '""' + delim + '""'
        for items in data[0]['Fields'].keys():
            line2 += delim + '"' + items + '"'
            line3 += delim + '"' + str(units[items]) + '"'
            line4 += delim + '"' + pro[items] + '"'
        line2 += '\n'    
        line3 += '\n'
        line4 += '\n'
        records = ""
        for recs in data:
            the_date = pakbus.nsec_to_time(recs['TimeOfRec'])
            the_date = dt.datetime.fromtimestamp(the_date) 
            records += '"' + str(the_date) + '"'
            records += delim + '"' + str(recs['RecNbr']) + '"'
            
            for items in data[0]['Fields'].keys():
                records += delim + '"' + str(recs['Fields'][items][0]) + '"'
            records += '\n'
        
        
        
        f = open(filename, "a")
        if not f_exists:
            f.write(line1)
            f.write(line2)
            f.write(line3)
            f.write(line4)
        
        f.write(records)
        f.close()
        return filename 
        

def main():
    """ the utility """
    print_center(UTILITY_TITLE, '-')
    try: 
        commands = csva.ArgClass(REQ_FLAGS, OPT_FLAGS, HELP_STRING)
    except RuntimeError, error_message:
        exit_on_failure(error_message[0])
        
    if commands.is_missing_flags():
        for items in commands.get_missing_flags():
            print_center(" ERROR: flag <" + items + "> is required ", "*")
        exit_on_failure()
    

    

    if not commands:
        c = LoggerLink()
        prompt(c)
    else:  
        if not ("--action" in commands.keys()):
            print_center("Error: no action given", "*")
            exit_on_failure() 
        if("--port" in commands.keys() and "--host" in commands.keys() ):
            c = LoggerLink(commands['--host'], commands["--port"])
        elif "--port" in commands.keys():
            c = LoggerLink(commands["--port"])
        elif "--host" in commands.keys():
            c = LoggerLink(commands['--host']) 
        else:
            c = LoggerLink()
        
      
        
        if "--filename" in commands.keys():
            f_name = commands["--filename"]
        else:
            f_name = "no file"
            
        if "--tablename" in commands.keys():
            t_name = commands["--tablename"]
        else:
            t_name = "no table"
        
        print action(c, action, f_name, t_name)
        
    c.unlink()
    print exit_on_success()



def action(c, command, f_name = "no file", t_name = "no table"): 
    """ preforms the action specifyed by command"""
    if command == "upload":
        ret = c.upload(f_name)
    elif command == "download":
        ret = c.download(f_name)
    elif command == "start":
        ret = c.progstart("CPU:" + f_name)
    elif command == "upStart":
        c.upload(f_name)
        ret = c.progstart("CPU:" + f_name)
    elif command == "status":
        ret = c.progstat()
    elif command == "fetch":
        ret = "comming soon"
    else :
        ret = "I dont know what that means"
    return ret
    
    

def prompt(c):
    """ an interactiveprompt for communicating with the data logger"""
    print_center("interactive prompt")
    
    while True:
        cmd = raw_input(">>> ")
        cmd_list = cmd.split(' ')
        if cmd_list[0] == "exit":
            print "So long, and thanks for all the fish!"
            return
        elif cmd_list[0] == "info":
            print c.info()
        elif cmd_list[0] == "help":
            print "dont panic"
        elif cmd_list[0] == "download":
            print cmd_list[1]
        elif cmd_list[0] == "upload":
            print cmd_list[1]
        elif cmd_list[0] == "host":
            print cmd_list[1]
        elif cmd_list[0] == "port":
            print cmd_list[1]
        elif cmd_list[0] == "earth":
            print "mostly harmless"
        elif cmd_list[0] == "milliways":
            print "the resterant at the end of the universe"
        elif cmd_list[0] == '*':
            if cmd_list[1] == '6' and cmd_list[2] == '9':
                print "42 " #(the universe may be fundamentally flawed)"
            else:
                print str((int(cmd_list[1])*int(cmd_list[2])))
        elif cmd_list[0] == '+':
            print str((int(cmd_list[1])+int(cmd_list[2])))
        elif cmd_list[0] == '-':
            print str((int(cmd_list[1])-int(cmd_list[2])))
        elif cmd_list[0] == '/':
            print str((int(cmd_list[1])/int(cmd_list[2])))

        

if __name__ == "__main__":
    main()

