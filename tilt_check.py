#!/usr/bin/python -tt
"""
tilt_check.py
rawser spicer
created: 2015/03/30
modified: 2015/03/30

        This utility checks the camera tilt by comparinng each image to 
    the last. Also checks to see that each time step is 1/2 hour.

    version 2015.03.30.1:
        version 1
    
"""
from os import listdir
import subprocess
from PIL import Image
import csv_lib.utility as util

def execute(command):
    """
    this function runs a system command
    
    arguments:
        command:    (string) the command to execute:
        
    returns an iterable list of the commnds output line by line
    """
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                                    stderr=subprocess.STDOUT)
    return iter(process.stdout.readline, b'')



HELP_STRING = """
Camera Tilt check utility
updated: 2015/03/30

    This utility checks the camera tilt by comparinng each image to 
the last. Also checks to see that each time step is 1/2 hour.

How to use:
    python tilt_check.py --image_dir=<path to images> --out_dir=<path to output>
    
Flags:
    --image_dir: the location of the cameras pictures
    --out_dir:   the output location
"""


class tilt_check(util.utility_base):
    def __init__(self):
        """
            sets up utility
        """
        super(tilt_check, self).__init__(" Checking Camera Tilt " ,
                    ("--image_dir", "--out_dir") ,
                    (),
                    HELP_STRING)
        self.img_dir = "/var/site/barrow/webcam1/view1/2014/"
        self.pre = "NGEE"
        self.ext = "jpg"
        self.success = " Check Complete "
        self.out_dir = "unset"
        
        
    def main(self):
        """
        main function does the checking of the images
        """
        self.img_dir = self.commands["--image_dir"]
        self.out_dir = self.commands["--out_dir"]
        img = Image.new('RGB',(300,75), 'green')
        img.save(self.out_dir + '/status.png')
        
        images = sorted(listdir(self.img_dir))
        images = [x for x in images if x[:4] == self.pre]
        images = images[-150:]
        images = [x for x in images if x[-3:] == self.ext]
        
        
        out_file = open(self.out_dir + "error.log", 'a')
        for idx in range(len(images)-1):
            
            # this calulates the time step 
            min_dif = abs(int(images[idx][images[idx].rfind('_') + \
                                          1:images[idx].rfind('-')]) \
                                          - int(images[idx+1][images[idx + \
                                          1].rfind('_') + \
                                          1:images[idx+1].rfind('-')]))
    
    
            
            # if the time step is not a normal one
            if not (min_dif == 70 or min_dif == 30 or min_dif == 2330):
                img = Image.new('RGB',(300,75), 'red')
                img.save('status.png')
                out_file.write(images[idx] + ',' + images[idx+1] + ',' + 
                                                    "timestep to large" + "\n")
                continue
        
        
            # the compare command
            compare = "compare  -channel red -metric RMSE " + self.img_dir \
                                                            + images[idx] \
                                                            + ' ' \
                                                            + self.img_dir \
                                                            +  images[idx+1] \
                                                            + " null"
            # check the difference 
            for line in execute(compare):
                num = float(line.strip()[line.find('(')+1:-1])
                if num > .225:
                    img = Image.new('RGB',(300,75), 'red')
                    img.save(self.out_dir + '/status.png')
                    out_file.write(images[idx] + ',' + images[idx+1] + ',' +
                                             "% difference:" + str(num) + '\n' )
            
        out_file.close()
        # delete temp files            
        execute("rm null*")
        
        ### End Main ###

if __name__ == "__main__":
    app = tilt_check()
    app.run()

