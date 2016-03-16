
from .baseClass import (ASTelement, ASTnode, ASTlist)
from . import valDefineMacro
from . import preamble




class NIheader(ASTnode):
    _fields = (
        "preamble",
        "body"
        )


class bodyStatements(ASTlist):pass







