import itertools

class ASTnode_base:
    _fields = NotImplemented
    def __init__(self, tokens):
        print(self.__class__)
        if not isinstance(tokens, list):
            tokens = tokens.asList()
        if len(tokens) == len(self._fields):
            for field, token in zip(self._fields, tokens):
                setattr(self, field, token)
        else:
            raise ValueError(
                "{}\n{}\n{}".format(
                    self.__class__,
                    len(tokens),
                    self._fields
                    )
                )
        

    def keys(self):
        return self._fields

    def values(self):
        for field in self.keys():
            yield getattr(self, field)

    def items(self):
        return zip(self.keys(), self.values())

class reprA:
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

class ASTnode(reprA, ASTnode_base):pass

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
