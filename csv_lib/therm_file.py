"""
dat_file.py
rawser spicer
created: 2014/09/03
modified: 2014/09/29

Part of DataPro Version 3

    This class represents the thermistor files used in datapro, the file creates
a table of rows with the values accessable as class varibles

    version 2014.09.29.1:
        added search functionus


"""
from six.moves import range

class ThermVals(object):
    """
    this represents a set of thermistor values
    """
    def __init__(self, res, temp, a, b, c):
        """
        initilizes values
        """
        self.resistance = float(res)
        self.temperature = float(temp)
        self.A = float(a)
        self.B = float(b)
        self.C = float(c)


class ThermFile(object):
    """
    this class repesents a thermistor file
    """
    def __init__(self, f_name):
        """
        loads the file

        arguments:
            file_name:      (string) the file name
        """
        self.name = "unnamed"
        self.standard = "unknown"
        self.table = []
        self.create_table(f_name)
        self.table = self.table[::-1]

    def create_table(self, f_name):
        """ Function doc """
        therm_file = open(f_name, "r")
        text = therm_file.read()
        therm_file.close()

        text = text.split('\n')
        self.name = text[0].split(",")[0]
        self.standard = text[0].split(",")[1]
        text = text[2:]
        for row in text:
            if row == "":
                continue
            cells = row.split(',')
            self.table.append(ThermVals(cells[0], cells[1], cells[2],
                                                  cells[3], cells[4]))
    def __getitem__(self, idx):
        """
            overlaods the __getitem__ function

        arguments:
            idx:    (int) the number of the row

        returns:
            the array reprenting the requested row
        """
        return self.table[idx]

    def seq_search(self, target):
        """
            returns the index to the valuse with the nearest resitance
        (rounds down)

        arguments:
            target:     (float) a target resistance in k-ohms

        returns:
            the index of the resistance, or a string if the index is not found
        """
        for index in range(len(self.table)):
            if index+1 >= len(self.table):
                break
            if target * 1000 >= self.table[index].resistance and \
               target * 1000 < self.table[index+1].resistance:
                return index
        return "not found"

    def bin_search(self, target):
        """
            finds the nearst index to a target resistance

        arguments:
            target:     (float) a target resistance in k-ohms

        returns:
            the index of the resistance, or a string if the index is not found
        """
        target *= 1000
        last = len(self.table)
        mid = int(last/2)
        first = 0
        mid_val = "undef"

        while mid_val != self.table[mid].resistance:
            mid_val = self.table[mid].resistance

            if mid_val == target:
                return mid
            if mid + 1 >= len(self.table):
                break
            if target > mid_val and target < self.table[mid + 1].resistance:
                val_range = self.table[mid + 1].resistance - mid_val
                offset = target - mid_val
                if offset/float(val_range) < .5:
                    return mid
                else:
                    return mid + 1
            if mid_val > target:
                last = mid
                mid = int(mid/2)
            else:
                first = mid
                mid = mid + int((last-mid)/2)

        return "not found"

