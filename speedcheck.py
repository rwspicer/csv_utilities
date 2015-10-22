"""
SpeedCheck Utility
Ross Spicer
created: 2015/09/01
modified: 2015/09/01

    <FILE DOCUMENTATION GOES HERE>

    v. 2015.09.01.1
        utility has been setup by Utility Setup Utility
"""
# Imports ______________________________________________________________________
import csv_lib.utility as util
from csv_lib.downloader import FileDownloader
### ADD OTHER IMPORTS HERE ###


# Classes ______________________________________________________________________
### ADD CLASSES HERE ###


# Utility Help String __________________________________________________________
HELP = """
    This Utility Help has been auto generated replace
this text with a description of the utility

    Example Usage:
    >>> python speedcheck.py --url=<value>

    Flags:
        --url
            <ADD DESCRTIPTION OF FLAG>


"""


# Utility ______________________________________________________________________
class SpeedCheck(util.utility_base):
    """
    This utility <description>
    """
    def __init__(self):
        """
        Sets up utility
        
        Preconditions:
            none        Postconditions:
            utility is ready to be run
        """
        super(SpeedCheck, self).__init__(" SpeedCheck " ,
            ['--url'],
            [],
            HELP)

    def main (self):
        """
        main body of utiliy.

        Preconditions:
        utility setup
            Postconditions:
            utility is run
        """
        download = FileDownloader(self.commands["--url"])
        download.download()
        print download.size
        print download.seconds
        print str(download.rate) + " Mbps"
        print str(download.Bps) + " Bps"
        #~ print str(download.rate * 8 ) + " bits/s"
        #~ print str(download.rate * 8 * .0000001) + " Mbits/s"


# Run Utility __________________________________________________________________
if __name__ == "__main__":
    SpeedCheck().run()
