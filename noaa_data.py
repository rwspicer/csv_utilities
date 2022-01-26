"""
noaa_data.py
rawser spicer
created: 2014/07/25
modified: 2014/07/31

        this utility will allow preciptation data to be pulled from a page on
    the noaa web site. This utility uses beautiful soup 4 for html parsing
    http://www.crummy.com/software/BeautifulSoup/. apt-get install python-bs4
    will install beautiful soup. The file contains a class for the data and
    an utility to use the class from the command line

    version 2014.8.4.1:
        fixed bug where using yesterday would use the current hour insted of 0

    version 2014.7.31.1:
        more documentation updates

    version 2014.07.29.4:
        updated documentation

    version 2014.07.29.3:
        fixed error caused when data is unavaible

    version 2014.07.29.2:
        fixed bug that has the data in the reverse order

    version 2014.07.29.1:
        the utility now works for saving data

    version 2014.07.28.1
        the bsic class has been compleated. Work will now begin on making a
    useful appilcation

    version 2014.01.05.1:
        added exmaple usage

"""
from httplib2 import Http
from bs4 import BeautifulSoup as bes
import datetime
import re

from csv_lib.csv_utilities import print_center, exit_on_failure, exit_on_success
import csv_lib.csv_file as csvf
import csv_lib.csv_args as csva


# maps the months to strings
mon_to_num = {"JAN":"1", "FEB":"2", "MAR":"3", "APR":"4", "MAY":"5",
              "JUN":"6", "JUL":"7", "AUG":"8", "SEP":"9", "OCT":"10",
              "NOV":"11","DEC":"12"}


class NCDCData(object):
    """
        this class can be used to get the data from one of the sites on
    www.ncdc.noaa.gov. Hourly percipatation and temperature are avaible for
    a given date.
    """
    def __init__(self):
        """
            initilizes the class
        """
        self.url = "str"
        self.html = "someday I'll be beautiful soup"
        self.ncdc_table = []
        self.parsed_table = []
        self.col_names = []
        self.save_name = "default.csv"
        self.ID="1007"
        self.units = ["UTC+0", "deg C", "mm"]

    def get_html(self):
        """
            gets the html from the noaa website
        """
        self.html = bes(Http().request(self.url)[1])


    def process_html(self):
        """
            processes the html into a more useable format
        """
        for item in self.html.find(id="hourly").thead.find_all('th'):
            self.col_names.append(item.text.strip().replace("Calculated",""))

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

        arguments:
            date:       <now|yesterday>(string) or (datetime.datetime)
            ID:         (int) the site id from the ncdc website

        exceptions:
            TypeError:  if the date type is not correct
        """
        self.ID=ID
        if (date == "now"):
            t_delta = datetime.timedelta(hours=1)
            date = datetime.datetime.now() - t_delta
            date = date.strftime("%Y%m%d%H")
        elif (date == "yesterday"):
            t_delta = datetime.timedelta(days=1)
            date = datetime.datetime.today() - t_delta
            date = date.replace(hour=0)
            date = date.strftime("%Y%m%d%H")
        elif type(date) is datetime.datetime:
            date = date.strftime("%Y%m%d%H")
        else:
            msg = 'Argument date must be "now", "yesterday", or a' + \
            ' datetime.datetime object'
            raise (TypeError, msg )


        self.url = "https://www.ncdc.noaa.gov/crn/station.htm?stationId="+ \
        ID + "&date=" + date + "&timeZoneID=US%2fAlaska&hours=24"


    def create_table(self):
        """
            creates the table from the parsed html
        """
        date = []
        temp = []
        precip = []

        for items in self.parsed_table:
            my_str = items[0]
            idx = my_str.find(',')+1
            date_str = my_str[idx:-4].replace("AM","0").replace("PM","12")
            date_str = mon_to_num[date_str[:3].upper()] + date_str[3:]
            reg_exp = r"^(\d+) (\d+) (\d+):00 (\d+)$"
            year = datetime.datetime.now().year
            mon, day, hour, am_pm = [t(s) for t , s in zip((int, int, int, int),
                                        re.search(reg_exp, date_str).groups())]

            hour += am_pm
            if hour == 12:
                hour = 0
            if hour == 24:
                hour = 12
            date.append(datetime.datetime(year, mon, day, hour))

            my_str = items[1]
            idx = my_str.find("F")+1
            my_str = my_str[idx:-2]
            try:
                temp.append(float(my_str))
            except:
                temp.append(float('nan'))

            my_str = items[2]
            idx = my_str.find("n")+1
            my_str = my_str[idx:-3]
            try:
                precip.append(float(my_str))
            except:
                precip.append(float('nan'))

        date.reverse()
        temp.reverse()
        precip.reverse()

        self.ncdc_table = [date, temp, precip]


    def set_filename(self, name):
        """
            allows the filename to be changed

        arguments:
            name:   (string) a filename
        """
        self.save_name = name


    def save_table(self, col = 2):
        """
            saves the table

        arguments:
            col:    <1|2>(int) the column to save to the data section of the
                output file
        """
        try:
            output = csvf.CsvFile(self.save_name)
        except IOError:
            raise (IOError, "NCDCData, error opening output file" )
        if not output.exists():
            h_str = "NCDC Site-" + self.ID + ',\n' + \
                                "TIMESTAMP," + self.col_names[col] + '\n' + \
                             self.units[0] + "," + self.units[col] + "\n" + \
                                ",Calculated\n"
            output.string_to_header(str(h_str))
            output[0] = self.ncdc_table[0]
            output[1] = self.ncdc_table[col]

        else:
            output.add_dates(self.ncdc_table[0])
            output.add_data(1, self.ncdc_table[col])

        output.save()


UTILITY_TITLE = " NCDC Data Parser "

OPT_FLAGS = ()
REQ_FLAGS = ("--time", "--filename", "--id", "--value")

HELP_STRING = """
        This Utility gets the teperature or precipitation data from a NOAA
    website.

    example usage:
        python noaa_data.py --time=yesterday --filenmae=<output>.csv
                            --id=1007 --value=temp

        --time = <"now"|"yesterday"|"yyyy/mm/dd">
                    the time and day you want the utility to get, can be "now",
                "yesterday", or a date in the YYYY-MM-DD formant

        --filename = <*.csv>
                    the file the data will be saved to

        --id = <*number*>
                    the id for the site (ie. 1007 for the AK Barrow 4 ENE site)

        --value = <temp|precip>
                    save the tempearure or precipatation
              """

def main():
    """
    runs the utility
    """
    print_center(UTILITY_TITLE, '-')
    try:
        commands = csva.ArgClass(REQ_FLAGS, OPT_FLAGS, HELP_STRING)
    except (RuntimeError, error_message ):
        exit_on_failure(error_message[0])

    if commands.is_missing_flags():
        for items in commands.get_missing_flags():
            print_center(" ERROR: flag <" + items + "> is required ", "*")
        exit_on_failure()

    time = commands["--time"]
    if not (time == "now" or time == "yesterday"):
        time = time.split('-')
        time = datetime.datetime(int(time[0]),int(time[1]),int(time[2]))

    if commands['--value'] == 'temp':
        col = 1
    else:
        col = 2

    my_data = NCDCData()
    my_data.construct_url(time, commands['--id'])
    my_data.get_html()
    my_data.process_html()
    my_data.create_table()
    my_data.set_filename(commands["--filename"])
    my_data.save_table(col)

    exit_on_success()




#---run utility----
if __name__ == "__main__":
    main()

