"""
icu.py

interval checking utility

IARC data processing project

rawser spicer
created: 2015/03/05
modified: 2014/03/05

	This utility can check a csv file, in the datapro output format, for any 
entries that do not lie on a standard interval provided as input.
"""



class ICU(util.utility_base):
	def __init__(self):
		super(datapro_v3, self).__init__(" Datapro 3.0 " ,
                    ("--infile", --"interval") ,
                    (),
                    "help tdb")
		print self.key_file
