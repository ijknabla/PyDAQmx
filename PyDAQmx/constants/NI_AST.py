class ASTnode:
    _fields = ("value", )
    def __init__(self, *args, **kwrds):
        for key in kwrds.keys():
            if key not in self._fields:
                raise NameError(
                    "invalid argument {key} : not in {self._fields}"\
                        .format(**vars())
                    )
        if len(args) + len(kwrds) != len(self._fields):
            raise ValueError(
                "argumente exceed expect {} got {args} and {kwrds}"\
                    .format(
                        len(self._fields),
                        **vars())
                )
        
        args_iter = iter(args)
        for attr in self._fields:
            try:
                setattr(self, attr, kwrds[attr])
            except KeyError:
                setattr(self, attr, next(args_iter))

    def __repr__(self):
        return "{self.__class__.__name__}({})"\
            .format(
                ", ".join("{} = {}".format(
                    field, getattr(self, field)) for field in self._fields
                          ),
                **vars()
                )

class Header(ASTnode):
    _fields = ("preamble", "content")

    @classmethod
    def handler(cls, tokens):
        return cls(*tokens.asList())

class Preamble(ASTnode):
    @classmethod
    def handler(cls, tokens):
        return cls(tokens.asList())

class Comment(ASTnode):
    @classmethod
    def handler(cls, tokens):
        return cls(*tokens.asList())