import pyparsing, types, operator

from . import pattern
from . import ast
from PyDAQmx.DAQmxConfig import dot_h_file

import os

def setParseAction(
    patternModule   = pattern,
    astModule       = ast
    ):
    for attr in set(dir(patternModule)) & set(dir(astModule)):
        patternObj, astObj = map(
            operator.attrgetter(attr),
            (patternModule, astModule)
            )
        if (isinstance(patternObj, types.ModuleType)
            and isinstance(astObj, types.ModuleType)):
            setParseAction(patternObj, astObj)

        if (isinstance(astObj, type)
            and issubclass(astObj, ast.ASTelement)):
            print(astObj)
            patternObj.setParseAction(astObj)

def parse_():
    parseFile = pattern.NIheader.parseFile
    try:
        return parseFile(dot_h_file)
    except FileNotFoundError:
        return parseFile(os.path.abspath("NIDAQmx.h"))
        

def parse():
    setParseAction()
    return parse_()

def printout():
    with open("result.txt", "w") as file:
        file.write(repr(parse()))