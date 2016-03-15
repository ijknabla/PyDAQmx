import itertools

class ASTelement:
    tab = "\t"



class ASTnode(ASTelement):
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
                "got {} tokens below\n"
                "{}".format(
                    len(tokens),
                    ("=" * 80 + "\n").join(map(str, tokens)),
                    **vars()
                    )
                )
    
    def __iter__(self):
        return self._fields

    def keys(self):
        return iter(self)

    def values(self):
        for field in self.keys():
            yield getattr(self, field)
    
    def items(self):
        return zip(self.keys(), self.values())

    def __repr__(self):
        return "\n".join(
            itertools.chain(
                ["{self.__class__.__name__}{".format(**vars())],
                map(
                    lambda txt : self.tab + txt,
                    (
                        ",\n".join(
                            "{} : {}".format(*field_value)
                            for field_value in self.items()
                            )
                        ).split("\n")
                ),
                ["}"]
                )
            )

class ASTlist(ASTelement):
    def __init__(self, tokens):
        if not isinstance(tokens, list):
            tokens = tokens.asList()
        self.list = list(tokens)

    def __iter__(self):
        return self.list

    def __repr__(self):
        return "\n".join(
            itertools.chain(
                ["{self.__class__.__name__}[".format(**vars())],
                map(
                    lambda txt : self.tab + txt,
                    (
                        ",\n".join(
                            map(repr, self)
                            )
                        ).split("\n")
                ),
                ["]"]
                )
            )


class NIheader(ASTnode):
    _fields = (
        "preamble",
        "body"
        )


class bodyStatements(ASTlist):pass



class ValDefineMacroStatement(ASTnode):
    _fields = (
        "title",
        "definition"
        )


class ValDefineMacroContent(ASTnode):
    _fields = (
        "label",
        "value",
        "comment"
        )



