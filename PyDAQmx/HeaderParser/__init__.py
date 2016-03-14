from .pattern import NIheader
from PyDAQmx.DAQmxConfig import dot_h_file

with open(dot_h_file) as file:
    text = file.read()

try:
    parsedResult = NIheader.parseString(text)[0]
except Exception as E:
    print(E)
 