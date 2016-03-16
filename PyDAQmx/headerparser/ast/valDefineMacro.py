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

class definitionLine(ASTnode):
    _fields = (
        "label",
        "expression",
        "detail"
        )