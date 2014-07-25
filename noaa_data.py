"""
noaa_data.py
rawser spicer
2014/07/25

    this utility will allow preciptation data to be pulled from a page on the 
noaa web site 
"""
from httplib2 import Http
import time
from bs4 import BeautifulSoup as bes
from datetime import datetime as dt
import re


mon_to_num = {"JAN":"1",
              "FEB":"2",
              "MAR":"3",
              "APR":"4",
              "MAY":"5",
              "JUN":"6",
              "JUL":"7",
              "AUG":"8",
              "SEP":"9",
              "OCT":"10",
              "NOV":"11",
              "DEC":"12"}


class NCDCData(object):
    """
    this is a class
    """

    def __init__(self):
        """
        this will do somthing, i dont know what yet
        """
        self.url = "str"
        self.html = "someday I'll be beautiful soup"
        self.ncdc_table = []
        self.parsed_table = []
        
    def get_html(self):
        """
        gets the html from the noaa website
        """
        self.html = bes(Http().request(self.url)[1])

    def process_html(self):
        """
        maybe removes newlines from html. beautiful soup may have a way of
        doing this
        """
        raw_data = self.html.find(id="hourly").tbody
        for row in raw_data.find_all('tr'):
            row_list = []
            for item in row.find_all('td'):
                row_list.append(item.text.encode('utf-8').replace('\r',"")
                                    .replace('\n',"").replace("\xc2","")
                                    .replace("\xb0","").replace("\xa0","")
                                    .replace("  ", "").strip())
            self.parsed_table.append(row_list)
                                           
        
                                      
        

    def construct_url(self, date = "now"):
        """
        makes the url to get the given dates url
        """
        if (date == "now"):
            date = time.strftime("%Y%m%d%H")
        self.url = "https://www.ncdc.noaa.gov/crn/station.htm?stationId=1007"+\
        "&date=" + date + "&timeZoneID=US%2fAlaska&hours=24"
        
        
        
    def create_table(self):
        """
        creates the table from the parsed html
        """
        for items in self.parsed_table:
            my_str = items[0]
            idx = my_str.find(',')+1
            date = my_str[idx:-4].replace("AM","0").replace("PM","12")
            date = mon_to_num[date[:3].upper()] + date[3:]
            reg_exp = r"^(\d+) (\d+) (\d+):00 (\d+)$"
            year = dt.now().year
            mon, day, hour, am_pm = [t(s) for t , s in zip((int, int, int, int),
                                        re.search(reg_exp,date).groups())]
            #print mon,day,year,hour,am_pm
            hour += am_pm
            if hour == 12:
                hour = 0
            if hour == 24:
                hour = 12
            date = dt(year, mon, day, hour)
            
            my_str = items[2]
            idx = my_str.find("n")+1
            my_str = my_str[idx:-3]
            precip = float(my_str)
            row = [date, precip]
            self.ncdc_table.append(row)
        
             
            
    def save_table(self):
        """
        saves the table
        """
        pass

a = NCDCData()
a.construct_url()
a.get_html()
a.process_html()
a.create_table()
for item in a.ncdc_table:
    print item


