#!/usr/bin/env python
"""
weather underground data formatting utility
wunder_fromatter.py
Rawser Spicer
created: 2014/04/16
modified: 2014/08/08

        this utility is designed to create links to upload data to weather
    underground. the format is specified here:
            http://wiki.wunderground.com/index.php/PWS_-_Upload_Protocol
            
    version 2014.8.8.1:
        updated documentation

    version 2014.5.1.1:
        added error checking for missing flags

    version 2014.4.24.1:
        added check for hourly data

    version 2014.4.18.1:
        the completed utility

    version 2014.4.16.1:
        set up utility basics
"""
from csv_lib.csv_utilities import print_center, exit_on_success, exit_on_failure
import csv_lib.csv_args as csva
import csv_lib.csv_file as csvf
import httplib2

def from_si(value, unit):
    """
        this function is for unit conversions from SI
    
    arguments:
        value:  (float)the input value
        unit:   (int) input units
    returns 
        the value in imperial units
    """
    if unit == "millibars":
        return value * .0295333727
    if unit == "celsius":
        return value * float(9.0/5) + 32
    if unit == "meters/second":
        return  value * 2.23694
    if unit == "degerees-rev":
        if value >= 180:
            return value - 180
        else:
            return value + 180
    return value

class WUURL(object):
    """
    this class represents a weather under ground upload url
    """
    def __init__(self):
        """
        initialize a url
        """
        self.base_url = "http://weatherstation.wunderground.com/" + \
                                "weatherstation/updateweatherstation.php"
        self.url_items = {}
        self.valid_keys = ("action", "ID", "PASSWORD", "dateutc", "winddir",
                          "windspeedmph", "windgustmph", "windgustdir",
                          "windspdmph_avg2m", "winddir_avg2m",
                          "windgustmph_10m", "windgustdir_10m",
                          "humidity", "dewptf", "temp*f", "rainin",
                          "dailyrainin", "baromin", "weather", "clouds",
                          "soiltemp*f", "soilmoisture*", "leafwetness*",
                          "solarradiation", "UV", "visibility", "indoortempf",
                          "indoorhumidity", "softwaretype")

    def __str__(self):
        """
        converst url to string
        """
        r_str = self.base_url + '?'
        for key in self.url_items.keys():
            r_str += key + '=' + \
                  self.url_items[key].replace(".", "%2E").replace("%", "%25") \
                  + '&'
        return r_str[:-1]

    def add_item(self, key, value):
        """
            adds an item to url
        
        arguments:
            key:    (string)
            value:  (string)
        """
        for items in self.valid_keys:
            loc = items.find('*')
            if loc != -1:
                prefix = items[:loc]
                try:
                    postfix = items[loc+1]
                except IndexError:
                    postfix = ""
                key_pre = key[:loc]
                end = -1
                while end == -1:
                    try:
                        int(key[loc])
                        loc += 1
                    except ValueError:
                        end = loc
                    except IndexError:
                        end = loc
                        break
                try:
                    key_post = key[end:]
                except IndexError:
                    key_post = ""

                if prefix == key_pre and postfix == key_post:
                    self.url_items[key] = value
                    return True
            else:
                if key == items:
                    self.url_items[key] = value
                    return True
        return False

    def send(self, show=False):
        """
            send the url
            
        arguments:
            show:    (bool) show the response
        """
        resp = httplib2.Http().request(str(self))
        if show:
            print resp[0]
            print resp[1]


UTILITY_TITLE = " weather underground data formatting utility "

OPT_FLAGS = ()
REQ_FLAGS = ("--ID", "--password", "--ref_file")

HELP_STRING = """
        This Utility is intended to generate an send a url containing
    information about different measurments to weather underground.

    flags:
        --ID=[ID as registered by wunderground.com]
        --password=[PASSWORD registered with this ID, case sensative]
        --ref_file=[a text file with a comma seperated list of measurments, 
                    their units, and csv file locations assoiated with the 
                    measurments]
              """

def main():
    """
    runs the utility
    """
    print_center(UTILITY_TITLE, '-')
    try:
        commands = csva.ArgClass(REQ_FLAGS, OPT_FLAGS, HELP_STRING)
    except RuntimeError, error_message:
        exit_on_failure(error_message[0])

    if commands.is_missing_flags():
        for items in commands.get_missing_flags():
            print_center(" ERROR: flag <" + items + "> is required ", "*")
        exit_on_failure()

    my_url = WUURL()
    f_name = commands["--ref_file"]
    my_url.add_item("ID", commands["--ID"]) # add ID
    my_url.add_item("PASSWORD", commands["--password"]) # add password
    my_url.add_item("action", "updateraw")

    my_file = open(f_name, 'r')
    fulltext = my_file.read()
    temp = csvf.CsvFile(fulltext.split('\n')[0].split(',')[2], True)
    idx = -1
    while True:
        first_date = temp[0][idx]
        if first_date.minute == 0 and first_date.second == 0:
            break
        idx -= 1

    my_url.add_item("dateutc", str(first_date.year) + '-' + \
                               str(first_date.month).zfill(2) + '-' + \
                               str(first_date.day).zfill(2) + '+' + \
                               str(first_date.hour).zfill(2) + "%3A" + \
                               str(first_date.minute).zfill(2) + "%3A" + \
                               str(first_date.second).zfill(2))

    if fulltext[-1] == '\n':
        fulltext = fulltext[:-1]
    for lines in fulltext.split('\n'):
        key, units, in_name = lines.split(',')
        temp = csvf.CsvFile(in_name)
        idx = -1
        while True:
            temp_date = temp[0][idx]
            if temp_date.minute == 0 and temp_date.second == 0:
                break
            idx -= 1

        if first_date == temp_date:
            my_url.add_item(key, str(from_si(temp[1][idx], units)))
        del temp

    print my_url
    my_url.send(True)

    exit_on_success()

#---run utility----
if __name__ == "__main__":
    main()








