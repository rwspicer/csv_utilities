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
import csv_lib.utility as util
import csv_lib.csv_file as csvf

import datetime as dt


class ICU(util.utility_base):
	def __init__(self):
		super(ICU, self).__init__(" Datapro 3.0 " ,
                    ("--infile", "--interval") ,
                    ("--first",),
                    "help tdb")
		self.infile = "not open"
		self.first = 0

	def main(self):
		self.load_infile()
		self.evaluate_errors()
		self.locate_first_line()
		self.interval_to_time_delta()
		
		dates = []
		data = []
		
		last = self.first
		dates.append(self.infile[0][last])
		data.append(self.infile[1][last])
		for i in range(self.first+1,len(self.infile[0])):
			for j in range(1,900):
				if self.infile[0][i] == self.infile[0][last] + \
																self.interval*j:
				 
					dates.append(self.infile[0][i])
					data.append(self.infile[1][i])
					last = i
					break
					
		self.infile.set_dates(dates)
		self.infile.set_data(1,data)
		self.infile.save()
				


	def load_infile(self):
		"""
		"""
		try:
			self.infile = csvf.CsvFile(self.commands["--infile"],
															must_exist=True)														
		except IOError:
			self.esrrors.set_error_state("I/O Error", "invalid input file")
			
	def locate_first_line(self):
		"""
		"""
		first = self.commands["--alt_data_file"]
		if first == "":
			self.first = 0
			return
		pass
	
	def interval_to_time_delta(self):
		i_tup = self.commands["--interval"].split(':')
		self.interval = dt.timedelta(hours = int(i_tup[0]),
									 minutes= int(i_tup[1]))
		
		


if __name__ == "__main__":
    utility = ICU()
    utility.run()
