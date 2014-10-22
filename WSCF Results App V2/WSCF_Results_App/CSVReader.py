import os

class CSVReader():
    filepath   = None
    csv_file   = None
    headers    = []

    def __init__(self, filepath):
        self.filepath = os.path.realpath(filepath)
        self.csv_file = open(self.filepath, "r")
        # set and clean headers
        self.headers = str.split(self.csv_file.readline(), ",")
        for i in range(0,len(self.headers)):
            self.headers[i] = self.headers[i].strip().rstrip().strip("\"").rstrip("\"")

    def getNext(self):
        newLine = self.csv_file.readline()
        if (newLine is None or not newLine):
            return None
        newRow = safeSplit(newLine, ",")
        return_values = []
        for i in range(0, len(newRow)):
            return_values.append(newRow[i].strip().rstrip().strip("\"").rstrip("\""))

        return return_values

    def getNextAsString(self):
        row = self.getNext()
        if row is None:
            return None

        return_str = ""
        for value in row:
            return_str += value + " "
        return return_str

    def getItem(self, header, row):
        for i in range(0, len(row)):
            if(self.headers[i] == header):
                return row[i]
        return None

    def getLongest(self, header):
        temp_reader = CSVReader(self.filepath)
        line = temp_reader.getNext()
        longest = 0
        while line != None:
            item = temp_reader.getItem(header, line)
            if(len(item) > longest):
                longest = len(item)

            line = temp_reader.getNext()

        return longest

def safeSplit(string, delimiter):
    start = 0
    quoteEscape = False
    results = []
    for i in range(0, len(string)):
        if string[i] == "\"":
            quoteEscape = quoteEscape == False
        if string[i] == delimiter and quoteEscape == False:
            results.append(string[start:i])
            start = i + 1
    results.append(string[start:])
    return results
