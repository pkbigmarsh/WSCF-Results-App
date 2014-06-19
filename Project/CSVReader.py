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
        newMap = {}
        for i in range(0, len(newRow)):
            newMap[self.headers[i]] = newRow[i].strip().rstrip().strip("\"").rstrip("\"")

        return newMap

    def getNextAsString(self):
        row = self.getNext()
        if row is None:
            return None

        return_str = ""
        for key in self.headers:
            return_str += row[key] + " "
        return return_str

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