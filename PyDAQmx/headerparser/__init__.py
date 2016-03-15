import pyparsing

from . import ast
from . import pattern
from PyDAQmx.DAQmxConfig import dot_h_file

def main():
    ASTelements = set(
        name 
        for name, obj in ast.__dict__.items()
        if (
            isinstance(obj, type)
            and issubclass(obj, ast.ASTelement)
            )
        )
    patterns = set(
        name 
        for name, obj in pattern.__dict__.items()
        if hasattr(obj, "setParseAction")
        )
    for name in ASTelements:
        print(name)
        if name in patterns:
            getattr(pattern, name).setParseAction(
                getattr(ast, name)
                )
        else:
            raise RuntimeError(
                "can't found pattern.{name}".format(**vars())
                )
    try:
        global parsedResult
        parsedResult = None
        parsedResult = pattern.NIheader.parseFile(dot_h_file)[0]
    except Exception as E:
        print(E)

main()
del main
 