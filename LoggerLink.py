"""
LoggerLink.py 
Rawser Spicer -- rwspicer@alaska.edu
Created: 2014/05/23
modified: 2014/07/31

        this appilcation and class are used for communicating with the 
    cr1000 datalogers. the commuincation wiht the logger uses the pakbus 
    package avaible at http://sourceforge.net/projects/pypak/files/ 
    
    version 2014.7.31.1:
        updates to documentation
  
    version 2014.6.2.2:
        the user interface has been compleated

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
import os


UTILITY_TITLE = " data logger communicator "

OPT_FLAGS = ("--port", "--host", "--filename", "--loggername", "--dir")
REQ_FLAGS = ("--action",)

HELP_STRING = """
        This utility is for communication with a datalogger. it can be 
    used for uploading and downloading programs, downloading data, and 
    veiwing the general status of the datalogger. 
    
        --action=<upload|downloadstatus|fetch|programs|tables>
                upload: upload a program file to the logger and start it
                download: downlaod a program file from the logger
                status: returns the status of the logger.
                fetch: fetch a data table from the logger
                programs: list the programs on the logger
                tables: list the tables on the logger
                
        --host=<host IP>
                The ip adderess of the computer the logger is linked to.
                
        --port=<port number>
                The number of the port the logger is on.
                
        --filename=<filename>
                The name of the file. Use with download, upload, 
            and start.

        --loggername=<loggername>
                the name of the logger use with fetch
                
        --dir=<directory to save .dat files to>
        
              """

class LoggerLink(object):
    """ 
    this class represents a connection to the data logger
    """
    
    def __init__(self, host = 'localhost', port = 7809, timeout = 30, 
                            logger_id = 0x001, computer_id = 0x802 ):
        """ 
            this initilizer function sets up the connection
            
        arguments:
            host:       (string) a string repesenting the ip for the connection
            port:       (int) the port number
            timeout:    (int) timeout value
            logger_id:  (int) the ID of the logger
            computer_id:(int) the id of the computer 
        """
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
        FileData, Response = pakbus.fileupload(self.link, self.l_id, self.c_id
                                                        , '.TDF')
        self.tabledef = pakbus.parse_tabledef(FileData)
        
        self.fetchprogs()
        
        
    def set_host(self, val):
        """ 
            set the host
        
        arguments:
            val:    (string) the new IP addr
        """
        self.host = val
        
        
    def set_port(self, val):
        """ 
            set the port
        
        arguments:
            port:   (int)the new port number
        """
        self.port = val
                                        
    def relink(self):
        """reestiblish the link with the data logger"""
        self.link = pakbus.open_socket(self.host, self.port
                                                 , self.timeout)
                                                 
    
    def ping(self):
        """
            pings the logger
        """
        rsp = {}
        while rsp == {}:
            rsp = pakbus.ping_node(self.link, self.l_id, self.c_id)
        return rsp
        
    
    def upload(self, filename, s_cond = 0x0000, swath = 0x0200):
        """
            upload a file to the logger
        
        arguments:
            filename:   (string) the file to be uploaded
            s_cond:     (int) the security condition
            swath:      (int) 
            
        returns:
            the response from the logger
        """
        self.ping()
        try:
            f = open(filename, 'rb')
        except IOError:
            return "File Error"
        f_contents = f.read()
        f.close()
        
        
        rsp = pakbus.filedownload(self.link, self.l_id, self.c_id, 
                            "CPU:"+filename, f_contents , s_cond, swath)
        self.fetchprogs()
        return rsp
        
                            
    def download(self, filename, s_cond = 0x0000):
        """ 
            downloads a file from the loger 
            
        arguments: 
            filename:   (string) the file name
            s_cond:     (int) the securit condition
        
        returns:
            the response from the logger
        """
        self.ping()
        filedata, response = pakbus.fileupload(self.link, self.l_id, self.c_id, 
                                        "CPU:"+filename ,s_cond)
                                        
        if response != 13:
            return response 
        f = open(filename,'w')
        #~ print filedata
        f.write(filedata)
        f.close()
        return response
                    
                            
    def unlink(self):
        """ 
            close the link to the data logger
        """
        pakbus.send(self.link, pakbus.pkt_bye_cmd(self.l_id, self.c_id))
        self.link.close()


    def info(self):
        """ 
            get the info for the link
            
        returns:
            a string containing iformation on the logger 
        """
        return "host = " + str(self.host) + '\n' + \
               "port = " + str(self.port) + '\n' + \
               "timeout = " + str(self.timeout) + '\n' + \
               "logger ID = " + str(self.l_id) + '\n' + \
               "computer ID = " + str(self.c_id) 
               
        
    def progstat(self):
        """
            gets the status of the program running on the logger
             
        return: 
            the status of the running program as a string
        """
        self.ping()
        pkt, TranNbr = pakbus.pkt_getprogstat_cmd(self.l_id, self.c_id)
        pakbus.send(self.link, pkt)
        hdr, msg = pakbus.wait_pkt(self.link, self.l_id, self.c_id, TranNbr)
        return msg
        
        
    def progstart(self, FileName):
        """
            starts the given progam
        
        arguments:
            FileName:   (string) the name of the program to start
        
        returns:
            the new status of the logger
        """
        self.ping()
        return self.progctrl(FileName,1)    
               
               
    def progctrl(self, FileName, FileCmd, SecurityCode = 0x0000
                     , TranNbr = None):
        """ 
            allows for commands to be sent to the data logger to control
        the program
        
        arguments:
            FileName:   (string) the file to start
            FileCmd:    <0|1> (int) 0 turns off program, 1 starts a program
            SecurityCode:   (int) security code
            TranNbr:        best left to default
        """
        pkt, t = pakbus.pkt_filecontrol_cmd(self.l_id, self.c_id,  FileName, 
                            FileCmd, SecurityCode, TranNbr)
        pakbus.send(self.link, pkt)
        hdr, msg = pakbus.wait_pkt(self.link,self.l_id, self.c_id, TranNbr)
        
        return msg
        
        
    def fetchprogs(self):
        """
            makes a list of the programs avaible on the data logger
        """
        FileData, Response = pakbus.fileupload(self.link, self.l_id, self.c_id 
                                                        , '.DIR')
        file_dir = pakbus.parse_filedir(FileData)
        for files in file_dir['files']:
            self.progs.append(files['FileName'])
            
    def listprogs(self):
        """ 
            get programs on the logger
        
        returns: 
            a list of the programs on the logger
        """
        return self.progs
        
        
    def refresh_tabledef(self):
        """
            refresh the table definition
        """
        self.ping()
        FileData, Response = pakbus.fileupload(self.link, self.l_id, self.c_id
                                                        , '.TDF')
        self.tabledef = pakbus.parse_tabledef(FileData)
        
        
    def listtables(self, refresh = False):
        """ 
            get list of tables
            
        returns:
            a list of the tables on the logger 
        """
        if (self.table_list == []) or refresh:
            self.ping()
            self.table_list = []
            for table in self.tabledef:
                self.table_list.append(table['Header']['TableName'])
        return self.table_list
        
        
    def fetchdata(self, t_name = "Snow", lastrecs = 0):
        """
            fetch the data form a table on the logger
        
        arguments:
            t_name:     (string) name of the table
            lastrecs:   (int) the last record recived
            
        returns:
            the data in an array
        """
        self.ping()
        array = [] 
        
        try:
            recs, more =  pakbus.collect_data(self.link, self.l_id, self.c_id
                                                       , self.tabledef
                                                       , t_name,P1 = 1)
        except StandardError:
            print "Error: table " + t_name + " was not found."
        if t_name == "Status" or t_name == "Public":
            return recs[0]['RecFrag']
        numRecs = recs[0]['RecFrag'][0]['RecNbr']  +1
        
        if lastrecs != 0:
            numRecs -= (lastrecs + 1)
        #~ print numRecs
        more = 1 
        while numRecs != 0:
            recs, more =  pakbus.collect_data(self.link, self.l_id, self.c_id
                                                       , self.tabledef
                                                       , t_name,P1 = numRecs)
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
        """ 
            gets the units for the table 
        
        arguments:
            t_name:     (string)the table
            
        returns: 
            information on the units
        """
        #~ self.ping()
        tableno = pakbus.get_TableNbr(self.tabledef, t_name) - 1
        
        units = {}
        processing = {}
        fields = self.tabledef[tableno]['Fields']
        for items in fields:
            units[items['FieldName']] = items['Units']
            processing[items['FieldName']] = items['Processing']
        return units, processing 
        
        
    def write(self, table, logger_name, w_dir = './', delim = ','):
        """ 
            writes given table to a file 
        
        arguments:
            table:          (stirng) the table
            logger_name:    (string) the logger name
            w_dir:          (string) the directory to write to
            delim:          (char) the delimiting char
            
        returns:
            the name of the file written
        """
        if not os.path.isdir(w_dir):
            os.makedirs(w_dir)
        
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
        
        # here is the case for status and public
        if table == "Status" or table == "Public":
            line1 = '"TOA5"' + delim + '"' + logger_name + '"' + delim + \
                 '"' + info["OSVer"].split('.')[0]  + '"' + delim + \
                 '"' + str(info["SerialNbr"]) + '"' + delim + \
                 '"' + info["OSVer"] + '"' + delim + \
                 '"' + info["ProgName"] + '"' + delim + \
                 '"' + str(info['ProgSig']) + '"' + delim + \
                 '"' + table + '"\n'
                 
                 
            f = open(w_dir+filename, "w")
            if not f_exists:
                f.write(line1)
            
            f.write(data)
            f.close()
            return filename 
        
        
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
        
        
        
        f = open(w_dir+filename, "a")
        if not f_exists:
            f.write(line1)
            f.write(line2)
            f.write(line3)
            f.write(line4)
        
        f.write(records)
        f.close()
        return filename 
        
    def write_all(self, logger_name, w_dir = './', delim=',',
                  inc_pub =False):
        """ 
            write all of the data to .dat files
        """
        for items in self.listtables():
            if items == 'Public' and not inc_pub:
                continue
            self.write(items, logger_name, w_dir, delim)
    
        

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
    

    

    #~ if not commands:
#~ 
        #~ c = LoggerLink()
        #~ prompt(c)
    #~ else:  
    #~ if not ("--action" in commands.keys()):
        #~ print_center("Error: no action given", "*")
        #~ exit_on_failure() 
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
        l_name = commands["--tablename"]
    else:
        l_name = "logger"
        
    if "--dir" in commands.keys():
        d_name = commands["--dir"]
    else:
        d_name = "./"
    
    print action(c, commands["--action"], f_name, l_name, d_name)
        
    c.unlink()
    print exit_on_success()



def action(c, command, f_name = "no file", l_name = "logger", 
                                                d_name = "./"): 
    """ preforms the action specifyed by command"""
    if command == "upload":
        ret = c.upload(f_name)
        if ret == 0:
            ret = c.progstart('CPU:' + f_name)
        elif ret == "File Error":
            ret = "File to upload was not found"
        else:
            ret = "upload error"
    elif command == "download":
        ret = c.download(f_name)
        if ret == 13:
            ret = "success"
        else:
            ret = "download error"
    elif command == "status":
        ret = c.progstat()
    elif command == "fetch":
        c.write_all(l_name, d_name)
        ret = "all data fetched"
    elif command == "programs":
        return c.listprogs()
    elif command == "tables":
        return c.listtables()
    else :
        ret = "Action is not Valid"
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

