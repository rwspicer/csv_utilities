"""
Alert Check 2.0 Utility
Ross Spicer
created: 2015/09/01
modified: 2015/09/03

        Alert check checks if the data from a data(table type) logger is
    current, and sends emails based on that state. based on alert check script
    by Amy Jacobs.
    
    v 2015.9.3.2r2
        now its really fixed
        fixed --check_file flag bug: changed from incrrect --check_url

    v. 2015.9.3.1
        version 1. All functionality works as tested. 
        
	v. 2015.9.1.1
		utility has been setup by Utility Setup Utility
"""
# Imports ______________________________________________________________________
import csv_lib.utility as util
from datetime import datetime, timedelta
import pickle
from csv_lib.downloader import FileDownloader
import smtplib
from email.mime.text import MIMEText

# Global Constants
STILL_ONLINE = 0
NOW_ONLINE = 1
STILL_OFFLINE = 2
NOW_OFFLINE = 3
UNCHANGED = 4
INIT_RUN = 5 

ONLINE = True
OFFLINE = False

status_lib = { STILL_ONLINE: "STILL ONLINE: No Report needed",
               NOW_ONLINE: "NOW ONLINE: Generating report",
               STILL_OFFLINE: "STILL OFFLINE: No Report needed",
               NOW_OFFLINE: "NOW OFFLINE: Generating report",
               UNCHANGED: "UNCHANGED: No Report needed",
               INIT_RUN: "INITAL RUN: No Report needed"}


# Classes ______________________________________________________________________
class SiteStatus(object):
    """ 
    class to represent the status of a site
    """
    
    def __init__ (self, timestamp, status):
        """
        sets the variables
        
        pre:
            timestamp a datetime object. status ONLINE/OFFLINE
        post:
            None
        """
        self.timestamp = timestamp
        self.status = status
        
class AlertCalc(object):
    """
    This class determines if an alert is needed. 
    """
    
    def __init__ (self, url, alert_time, status_dir = ""):
        """ 
        initializes variables
        
        pre:
            url should be a URL or file path, alert time should be an integer,
        and status_dir needs to be a path to an existing directory. 
        
        post:
            variables set up
        """
        self.date_format = '"%Y-%m-%d %H:%M:%S"'
        self.url = url
        self.alert_time = alert_time
        self.tag = url[url.rfind('/')+1:url.rfind('.')]
        print self.url
        self.last_data_time = None
        self.s_dir = status_dir
        
    def get_last_data_time (self):
        """
        gets the last timestamp from a logger .dat file
        
        pre:
            self.url should exist. 
        postconditions:
            self.last_data_time is a datetime
        """
        if self.last_data_time == None:
            #~ print self.url[:self.url.find(':')]
            if self.url[:self.url.find(':')] == "http"  or \
               self.url[:self.url.find(':')] == "https" or \
               self.url[:self.url.find(':')] == "ftp" : 
                
                FD = FileDownloader(self.url)
                FD.download()
                data = FD.data
            else: 
                data = open(self.url, 'r').read()
            current_date = data.replace('\r',' ').\
                                   split('\n')[-1].split(',')[0]
            if current_date == "" :
                current_date = data.replace('\r',' ').\
                                split('\n')[-2].split(',')[0]
            self.last_data_time = datetime.strptime(current_date, 
                                                    self.date_format) 
        return self.last_data_time
    
    def open_status (self):
        """ 
        loads the last status 
        pre:
            file should exist
        post:
            returns a SiteStatus object
        """
        fd = open(self.s_dir + "alert_check_status_" + self.tag + ".pckl", 'r')
        pt = pickle.load(fd)
        fd.close()
        return pt
    
    def save_status (self, status):
        """ 
        saves the status
        pre:
            status is a SiteStatus object and self.s_dir exists
        post:
            status is saved to self.s_dir
        """
        fd = open(self.s_dir + "alert_check_status_" + self.tag + ".pckl", 'wb')
        pickle.dump(status, fd)
        fd.close()

    def calc_alert (self):
        """ 
        calculates if an alert is needed for the site
        
        pre:
            none
        post:
            a state of UNCHANGED, NOW_ONLINE, or NO OFFLINE is returned.  
        """
        # get important times
        self.get_last_data_time()
        timestamp = datetime.now()
        
        # get last status
        try:
            old_status = self.open_status()
        except IOError:
            new_status = SiteStatus(timestamp, ONLINE) # the station is assumed 
                                                        # to be online
            self.save_status(new_status)
            return INIT_RUN # a report is not needed
        
        # calculate alert
        status = ONLINE
        state = UNCHANGED
        hours = int((timestamp - self.last_data_time).total_seconds()/3600.0) 
        if hours >= self.alert_time:
            if old_status.status == ONLINE:
                state = NOW_OFFLINE
            status = OFFLINE
        elif hours < self.alert_time:
            if old_status.status == OFFLINE:
                state = NOW_ONLINE
            status = ONLINE
                
        self.save_status(SiteStatus(self.last_data_time, status))
        return state

            


# Utility Help String __________________________________________________________
HELP = """
	This Utility Help has been auto generated replace
this text with a description of the utility

	Example Usage:
	>>> python alert_check_2_0.py --check_file=<path or URL> --site=<value>
    --alert_time=<value> --recipients=<list> --sender=<value> --state_dir=<path>
    --

	Flags:
		--check_file
                file path or URL(supports http, https, and ftp) of data file to 
            check
		--alert_time
            #number of hours to send alert after
		--recipients
			comma separated list of emails alert is sent to 
		--sender
			email address the alert should be sent from
        --site
            the site being checked
        --state_dir
            directory to save the last known state to. 

"""


# Utility ______________________________________________________________________
class AlertCheck2(util.utility_base):
    """
    This utility <description>
    """
    def __init__(self):
        """
        Sets up utility
        
        Preconditions:
            none		Postconditions:
            utility is ready to be run
        """
        super(AlertCheck2, self).__init__(" Alert Check 2.0 " ,
            ['--site',
             '--check_file', 
             '--alert_time', 
             '--recipients', 
             '--sender',
             '--state_dir'],
            [],
            HELP)


    def main (self):
        """
        main body of utiliy.
        
        Preconditions:
            utility setup, commands should fit their described types described 
        in the help string. 
        
        Postconditions:
            utility is run, an email is sent if necessary
        """
        
        
        alert = AlertCalc(self.commands["--check_file"],
                          int(self.commands["--alert_time"]))
        
        state = alert.calc_alert()
        print status_lib[state]
        if state == UNCHANGED or state == INIT_RUN:
            return
        
        #calculate utc offset
        localtime = datetime.now()
        utctime = datetime.utcnow()
        tzoffset = localtime.hour - utctime.hour 
        tzstr =  "UTC" + str(tzoffset)
        
        # specialization for Alaska 
        if tzstr == "UTC-9":
            tzstr = "AKST"
        elif tzstr == "UTC-8":
            tzstr = "AKDT"
       
        # create message 
        site = self.commands["--site"]
        msg = site + " real-time status as of " + \
               localtime.strftime("%Y-%m-%d %H:%M") + ":00 "+  tzstr +\
               "\n\n" + "__STATUS__\n\n" + \
               "Last reported hourly diagnostics timestamps: \n" + site + \
               ": " + alert.last_data_time.strftime("%Y-%m-%d %H:%M:%S") + \
               " " + tzstr + "\n"
        sender = self.commands["--sender"]
        recipients = self.commands["--recipients"]
        
        
        if state == NOW_OFFLINE:
            temp = "The " + site + " sensor has exceeded " + \
                   self.commands["--alert_time"] + " hours since its" + \
                   " last report."
            msg = MIMEText(msg.replace('__STATUS__', temp))
            msg['Subject'] = "Sensor Alert: " + site + " offline"
        elif state == NOW_ONLINE:
            temp = "The " + site + " sensor is now current"
            msg = MIMEText(msg.replace('__STATUS__', temp))
            msg['Subject'] = "Sensor Alert: " + site + " online"
        
        msg["From"] = sender
        msg["To"] = recipients
        
        #send messege
        server = smtplib.SMTP('smtp.uaf.edu')
        server.sendmail(sender,recipients.split(','),msg.as_string())
        server.quit()
        
        

# Run Utility __________________________________________________________________
if __name__ == "__main__":
	AlertCheck2().run()
