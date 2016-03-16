
import pyparsing, functools, types

def setname(name):
    if not isinstance(name, str):raise TypeError
    target = globals()[name]
    target.setName(name)

class KeywordSlot:
    def __init__(self):
        self.allkeyword = set()

    def __call__(self, cls):
        if not issubclass(cls, pyparsing.Keyword):
            raise TypeError("must be pyparsing.Keyword")
        
        @functools.wraps(cls.__init__)
        def initializer(target, keyword, *args, **kwrds):
            self.allkeyword.add(target)
            cls.__init__(target, keyword, *args, **kwrds)

        return type(
            "{self.__class__.__name__}({cls.__name__})"\
                .format(**vars()),
            (cls,),
            {"__init__" : initializer}
            )

    def getallkeyword(self):
        if self.allkeyword:
            return pyparsing.MatchFirst(*self.allkeyword)
        else:
            class DummyParserElement(pyparsing.ParserElement):
                def __invert__(self):
                    return self
                def __add__(self, other):
                    return other
                def __repr__(self):
                    return "dummyParserElement"

            return DummyParserElement()