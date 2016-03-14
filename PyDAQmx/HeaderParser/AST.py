import itertools

class ASTnode_base:
    _fields = NotImplemented
    def __init__(self, tokens):
        if not isinstance(tokens, list):
            tokens = tokens.asList()
        if len(tokens) == len(self._fields):
            for field, token in zip(self._fields, tokens):
                setattr(self, field, token)
        else:
            raise ValueError(
                "{self.__class__} expect {self._fields}\n"
                "got {tokens}".format(
                    **vars()
                    )
                )
        

    def keys(self):
        return self._fields
    def values(self):
        for field in self.keys():
            yield getattr(self, field)
    def items(self):
        return zip(self.keys(), self.values())

class tree_repr:
    tab = " "

    def __repr__(self):
        return "\n".join(
            itertools.chain(
                ["{self.__class__.__name__} (".format(**vars())],
                map(
                    lambda txt : self.tab + txt,
                    (
                        ",\n".join(
                            "{} : {}".format(*field_value)
                            for field_value in self.items()
                            )
                        ).split("\n")
                ),
                [")"]
                )
            )

class ASTnode(tree_repr, ASTnode_base):pass

class ValDefineMacroStatement(ASTnode):
    _fields = (
        "title",
        "content"
        )

class ValDefineMacroTitle(ASTnode):
    pass

class ValDefineMacroContent(ASTnode):
    pass

class NIheader(ASTnode):
    _fields = (
        "preamble",
        "body"
        )

class ifndefMacroStatement(ASTnode):
    _fields = (
        "macroLabel", "code"
        )

class Preamble(ASTnode):
    @classmethod
    def handler(cls, tokens):
        return cls(tokens.asList())

class Comment(ASTnode):
    @classmethod
    def handler(cls, tokens):
        return cls(*tokens.asList())
