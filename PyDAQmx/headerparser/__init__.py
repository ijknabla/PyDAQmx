import pyparsing

from . import ast
from . import pattern
from PyDAQmx.DAQmxConfig import dot_h_file

def main():
    ASTelements = set(
        name 
        for name, obj in ast.__dict__.items()
        if isinstance(obj, ast.ASTelement)
        )
    patterns = set(
        name 
        for name, obj in pattern.__dict__.items()
        if hasattr(obj, "setParseAction")
        )
    for name in ASTelements:
        if name in patterns:
            getattr(pattern, name).setParseAction(
                getattr(ast, name)
                )
    try:
        global parsedResult
        parsedResult = None
        with open(dot_h_file) as file:
            parsedResult = pattern.NIheader.parseFile(file.read())[0]
    except Exception as E:
        print(E)

main()
del main
 