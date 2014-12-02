"""
ross spicer
2014/08/05
this is an example of how the new utility_base class works
"""
import csv_lib.utility as util


class my_utility(util.utility_base):
    def __init__(self, title , r_args, o_args, help):
        
        super(my_utility, self).__init__(title , r_args,("--b",), help)
        self.title = " my adder "

    def main(self):
        self.a = int(self.commands["--a"])
        
        try:
            self.b = int(self.commands["--b"])
        except ValueError: #<-- int() wont work on '' which is bing returned
            self.b = 0
        
        self.my_addition()
            
    def my_addition(self):
        ans =self.a +self.b
        self.print_center(str(self.a) + " + " + str(self.b) +  " = " + str(ans))
        
        
a = my_utility("title",("--a",),(),"help")
a.run()

