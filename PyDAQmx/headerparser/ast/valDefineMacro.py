from .baseClass import (ASTelement, ASTnode, ASTlist)

class statement(ASTnode):
    _fields = (
        "title",
        "contents"
        )

class title(ASTlist):pass

class contents(ASTlist):pass

class content(ASTnode):
    _fields = (
        "header",
        "definition"
        )

class header(ASTlist):pass

class definition(ASTlist):pass

class definitionLineBase(ASTnode):
    pass

class definitionLine(definitionLineBase):
    _fields = (
        "label",
        "expression",
        "detail"
        )

class definitionLineNotDetail(definitionLineBase):
    _fields = (
        "label",
        "expression"
        )