"""
TutorialUtility
rawser spicer
2014/11/04
"""
import csv_lib.utility as util # for utility_base
import datetime as dt          # for getting the current date/time
from random import randint     # generating random int
import csv_lib.csv_file as csvf # for csv files


class TutorialUtility(util.utility_base):
    """
        this is a tutorial utility
    """
    def __init__(self):
        """
            initlize utility
        """
        # calls utility_base's __init__
        super(TutorialUtility, self).__init__(" Tutorial Utility " , # title
                    ("--mult_1", "--pow_1" ),          # required argument flags
                    ("--mult_2", "--pow_2","--const"), # optional argument flags
                     "replace with help")              # help string


    def main(self):
        """
            body of utility
        """
        #~ for key in self.commands.keys():
            #~ print key + " = " + self.commands[key]

        num = randint(0,99)
        #~ num = 10
        print( "the random # is " + str(num))


        # required arguments
        # create a string representation of our equation
        eq = self.commands["--mult_1"] + "(" + str(num) + "^" + \
             self.commands["--pow_1"] + ")"

        # sets commands.return_func to intify which has commands[] operator
        # return int representations of the value. Floatify and
        # stringify(default) are also defined, or you can set your own
        # function(more on this later)
        self.commands.return_func = self.commands.intify
        ans = self.commands["--mult_1"] * (num ** self.commands["--pow_1"])

        # update equation for optional arguments
        #~ self.commands.return_func = self.commands.stringify # we need default
                                                               # values
        self.commands.return_func = self.my_stringify
        eq += " + " + self.commands["--mult_2"] + "(" + str(num) + "^" + \
             self.commands["--pow_2"] + ") + " + self.commands["--const"]


        #~ self.commands.return_func = self.commands.intify # we need default
                                                            # values
        self.commands.return_func = self.my_intify
        ans += self.commands["--mult_2"] * (num ** self.commands["--pow_2"]) +\
               self.commands["--const"]

        print  (eq + " = " + str(ans) )

        print ("logging to tutorial_log.csv")

        myfile = csvf.CsvFile("tutorial_log.csv", False, opti=True)
        # opti = True will olny load the last row in a file
        # use full if adding to file and not processign the data in a file

        if not myfile.exists(): # see if my file exists
            #the header should be a list of lists of strings
            header = [[ "tutorial outputs\n"], #newlines are important
            ["timestamp", "random num", "m1", "p1", "m2", "p2","c","output\n"]]
            myfile.set_header(header)

        now = dt.datetime.now()
        myfile.add_dates(now)
        myfile.add_data(1,num)
        myfile.add_data(2,self.commands["--mult_1"])
        myfile.add_data(3,self.commands["--pow_1"])
        myfile.add_data(4,self.commands["--mult_2"])
        myfile.add_data(5,self.commands["--pow_2"])
        myfile.add_data(6,self.commands["--const"])
        myfile.add_data(7,ans)

        myfile.append()


    def my_stringify(self, value):
        if value == "":
            value = "0"
        return str(value)


    def my_intify(self, value):
        if value == "":
            value = 0
        return int(value)

# run the utility
if __name__ == "__main__":
    the_utility = TutorialUtility() # create utility instance
    the_utility.run()               # run() is defined in utility_base
