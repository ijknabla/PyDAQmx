import PyDAQmx

import itertools, functools
import collections

class ASTelement: pass

class NestedRepr:
    tab = " "

    def __repr__(self):
        if   isinstance(self, collections.Mapping):
            return "\n".join(
                itertools.chain(
                    ["{self.__class__.__name__}{}".format("{", **vars())],
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
        elif isinstance(self, collections.abc.Sequence):
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
            

class ASTnode(ASTelement, NestedRepr, dict):
    _fields = NotImplemented
    def __init__(self, tokens):
        if hasattr(tokens, "asList"):
            tokens = tokens.asList()
        if len(tokens) == len(self._fields):
            super().__init__(zip(self._fields, tokens))
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
        return iter(self._fields)

    def keys(self):
        return iter(self)

    def values(self):
        for key in self.keys():
            yield self[key]

    def items(self):
        return zip(self.keys(), self.values())

    def __setattr__(self, attr, value):
        if attr in self._fields:
            self[attr] = value
        else:
            super().__setattr__(attr, value)
     
    def __getattr__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError:
            return self[attr]



class ASTlist(ASTelement, NestedRepr, collections.UserList):
    
    def __init__(self, tokens = []):

        if hasattr(tokens, "asList"):
            tokens = tokens.asList()

        super().__init__(tokens)