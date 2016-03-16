import pyparsing, types, operator

from . import pattern
from . import ast
from PyDAQmx.DAQmxConfig import dot_h_file

def combine():
    patternSubModuleDict = dict(
        (name, module)
        for name, module in pattern.__dict__.items()
        if isinstance(module, types.ModuleType)
        )
    astSubModuleDict = dict(
        (name, module)
        for name, module in ast.__dict__.items()
        if isinstance(module, types.ModuleType)
        )
    for name in (
        set(patternSubModuleDict.keys())
        & set(astSubModuleDict.keys())
        ):
        patternSubModule    = patternSubModuleDict[name]
        astSubModule        = astSubModuleDict[name]
        for attr, astElement in filter(
            (lambda f : lambda xs : f(*xs))(
                lambda attr, obj : isinstance(obj, type) and issubclass(obj, ast.ASTelement)
                ),
            astSubModule.__dict__.items()
            ):
            try:
                patternElement = getattr(patternSubModule, attr)
                try:
                    patternElement.setParseAction(astElement)             
                except AttributeError:
                    raise RuntimeError
            except AttributeError:
                pass

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
    return pattern.NIheader.parseFile(dot_h_file)

def parse():
    setParseAction()
    return parse_()

def printout():
    with open("result.txt", "w") as file:
        file.write(repr(parse()))