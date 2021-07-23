"""
downloader.py
Ross Spicer
created: 2015/09/02
updated: 2015/09/02

        FileDownloader is a class for downloading and saving a file from a URL
    with built in download speed measurement. 
"""

#~ import urllib2
#~ from datetime import datetime
from __future__ import absolute_import
import requests

class FileDownloader (object):
    """ Class doc """
    
    def __init__ (self, URL):
        """ Class initialiser """
        self.url = URL
    
    def download (self):
        """ Function doc """
        
        self.response = requests.get(self.url)
        if self.response.reason != 'OK':
            raise Exception
        #~ time = (end - start).seconds * 1000000 + (end - start).microseconds
        #~ time = (end - start).total_seconds()
        #~ time /= 1000000.0
        self.seconds = self.response.elapsed.total_seconds()
        self.data = self.response.content
        
        length = len(self.data)
        self.Bps = (length/self.seconds) # Bytes/second
        self.Mbps = self.Bps * 8E-6 # Megabits/second
        self.rate = self.Mbps # Megabits/second
        
    def save(self, filename): 
        """ Function doc """
        fd = open(filename, 'w')
        fd.write(self.data)
        fd.close()
    
