"""
noaa_data.py
rawser spicer
created: 2014/07/25
modified: 2014/07/28

        this utility will allow preciptation data to be pulled from a page on 
    the noaa web site. This utility uses beautiful soup 4 for html parsing 
    http://www.crummy.com/software/BeautifulSoup/

    version 2014.07.28.1
        the bsic class has been compleated. Work will now begin on making a 
    useful appilcation
    
"""
from httplib2 import Http
from bs4 import BeautifulSoup as bes
import datetime
import re


mon_to_num = {"JAN":"1", "FEB":"2", "MAR":"3", "APR":"4", "MAY":"5",
                      "JUN":"6", "JUL":"7", "AUG":"8", "SEP":"9", "OCT":"10",
                      "NOV":"11","DEC":"12"}


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
                                           
                                           
    def construct_url(self, date = "now", ID = "1007"):
        """
        makes the url to get the given dates url
        """
        if (date == "now"):
            date = datetime.datetime.now().strftime("%Y%m%d%H")
        elif (date == "yesterday"):
            t_delta = datetime.timedelta(days=1)
            date = datetime.datetime.now() - t_delta
            date = date.strftime("%Y%m%d%H")
        elif type(date) is datetime.datetime:
            date = date.strftime("%Y%m%d%H")
        else:
            msg = 'Argument date must be "now", "yesterday", or a' + \
            ' datetime.datetime object' 
            raise TypeError, msg
            
        
        self.url = "https://www.ncdc.noaa.gov/crn/station.htm?stationId="+ \
        ID + "&date=" + date + "&timeZoneID=US%2fAlaska&hours=24"
        
        
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
            year = datetime.datetime.now().year
            mon, day, hour, am_pm = [t(s) for t , s in zip((int, int, int, int),
                                        re.search(reg_exp,date).groups())]
            #print mon,day,year,hour,am_pm
            hour += am_pm
            if hour == 12:
                hour = 0
            if hour == 24:
                hour = 12
            date = datetime.datetime(year, mon, day, hour)

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


