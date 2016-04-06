
from .baseClass import (ASTelement, ASTnode, ASTlist)
from . import valDefineMacro
from . import preamble




class NIheader(ASTnode):
    _fields = (
        "preamble",
        "statements"
        )


class statements(ASTlist):pass







