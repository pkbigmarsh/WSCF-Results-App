import os
from CSVReader import *

individualFilePath = '../Info/tournamentresultsposting/individual_k12.TXT'

result = CSVReader(individualFilePath)
print result.headers
print result.getNext()