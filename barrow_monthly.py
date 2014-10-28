"""
noaa_monthly.py
rawser spicer
created: 2014/10/27
modified: 2014/10/28

 
    
"""
from httplib2 import Http
from datetime import date
import threading
import os

import csv_lib.utility as util





class NCDCCsv(object):
    """
        this class can be used to get the data from one of the sites on 
    www.ncdc.noaa.gov. This data will be in csv file format for a give month and
    year.
    """
    def __init__(self, year, month, s_dir = ""):
        """
            initilizes the class
        """
        if len(str(month)) == 1:
            month = "0" + str(month)
        
        self.url = "http://www.ncdc.noaa.gov/crn/newmonthsummary?"+\
                    "station_id=1007&yyyymm=" + str(year) + str(month)+\
                    "&format=csv"
        self.response = ""
  
        self.save_name = s_dir + "barrow_4_ENE_" + str(year) + str(month) + \
                        ".csv"
        
    def get_csv(self):
        """
            gets the .csv from the noaa website
        """
        while(True):
            self.response = Http().request(self.url)[1]
            if self.response[0] == '#':
                self.response = self.response.replace("*&nbsp","")
                self.response = self.response.replace(";","")
                break
                          
    def save(self):
        """
            saves the data to a file
        """
        outfile = open(self.save_name, "w")
        outfile.write(self.response)
        outfile.close()
        
HELP_STRING = """
    this utility can get the .csv data for the barrow site 
    from the noaa web site form feb 2008 to now. 
    
    example usage:
        python barrow_monthly.py --out_path=<path>
    
    flag info
        --out_path:         <<path_to_file output>> a path to where outputs
                            will be written

        optional (must bot be used)
        --start_year:       (int)<year> a year to start at
        --start_month:      (int)<mon> a montin to star at
              """

class barrow_monthly(util.utility_base):
    """
    this utility can get the .csv data for the barrow site 
    from the noaa web site form feb 2008 to now.
    """
    def __init__(self):
        """
        set up the utility
        
        arugments:
            year:   (int) the start year
            mon:    (int) the start month
            
        post-conditions:
            the utility is ready to run
        """
        super(barrow_monthly, self).__init__(" Barrow monthly data fetcher " ,
                ("--out_path",) ,("--start_year","--start_month"), HELP_STRING)
        self.f_year = 2008
        self.f_mon = 2
        
        self.s_dir = self.commands["--out_path"]
        if len(self.commands) == 2:
            self.errors.set_error_state("Optional Flag Error", 
                    "--start_year and --start_month must both be set if one is")
        self.evaluate_errors()
        if len(self.commands) == 3:
            cmd_year = int(self.commands["--start_year"])
            cmd_mon =  int(self.commands["--start_month"])
            
            if cmd_year >= self.f_year:
                self.f_year = cmd_year
            if cmd_mon >= self.f_mon:
                self.f_mon = cmd_mon
        
        
        if not os.path.exists(self.s_dir):
            os.makedirs(self.S_dir)
        self.m_dict = {} 
        
        
    def main(self):
        """
        main body
            
        pre-conditions:
            f_year needs to be set to a valid date for the site (>2008)
            f_mon nees to be a vaild month for the site (>2)
            
        """
        todays_year = date.today().year
        todays_mon = date.today().month
        
        p_year = self.f_year
        p_mon = self.f_mon
        
        print "Messege: getting data from www.ncdc.noaa.gov" + \
              "and it may take some time"
        while True:
            if p_year == todays_year and p_mon == todays_mon:
                break
            while threading.activeCount() > 10:
                pass
            
            t= threading.Thread(target=self.p_func, args=(p_year,p_mon))
            t.start()
            
            
            p_mon += 1
            
            if p_mon > 12:
                p_year += 1
                p_mon = 1
        
        
        while threading.activeCount() > 1:
            pass
        print "Messege: all data recived, compiling final output"
        self.write_all(todays_year,todays_mon)
        
    def write_all(self, todays_year, todays_mon):
        """
        writes all of the data to one .csv file
        
        arugments:
            todays_year:    (int)
            todats_month:   (int)
        
        pre-conditions:
            m_dict must be filled with data and not have any thing being added
            to it by a thread
        """

        header = "barrow_4_ENE_" + str(self.f_year)+str(self.f_mon).zfill(2)\
                                 +"_"+ str(todays_year)+str(todays_mon).zfill(2)
        f_stream = open(self.s_dir+"_"+header+".csv","w")
        header += "\nDate,AvgTemp,MaxTemp,MaxTempTime,MinTemp,MinTempTime," +\
                 "MM2Temp,TotPrecip,MaxHourlyPrecip,MaxSubhourlyPrecip,"+\
                 "MaxHourlyWind,Max10sWind,TotalSR,MaxSR,MaxSRTime\n"
        f_stream.write(header)
        for idx in self.m_dict:
            write_data = self.m_dict[idx].rstrip()
            year_mon_str = str(idx)[:4] + "-" +str(idx)[4:].zfill(2) + "-"
            write_data = year_mon_str + write_data
            write_data = write_data.replace('\n', '\n'+year_mon_str)
            write_data += '\n'
            f_stream.write(write_data)
            
        f_stream.close()
    
        
    def p_func(self, year, month):
        """
        this function processes a month
        
        arguments:
            year:   (int)
            mon:    (int)
        """
        obj = NCDCCsv(year, month, self.s_dir)
        obj.get_csv()
        obj.save()
        text = obj.response[obj.response.find("\n")+1:]
        self.m_dict[str(year)+str(month)] = text[text.find("\n")+1:]
        
        
if __name__ == "__main__":
    the_utility = barrow_monthly()
    the_utility.run()
        
        
        
        
        
        
        
        
        
        

