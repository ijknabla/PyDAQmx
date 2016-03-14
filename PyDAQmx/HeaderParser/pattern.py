﻿from . import AST
import pyparsing as pp

import functools, operator

def setaction(name):
    target = globals()[name]
    target.setParseAction(getattr(AST, name))

def setname(name):
    target = globals()[name]
    target.setName(name)

class KeywordSlot:
    def __init__(self):
        self.allkeyword = set()

    def __call__(self, cls):
        if not issubclass(cls, pp.Keyword):
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
        return pp.MatchFirst(*KEYWORDSLOT.allkeyword)

KEYWORDSLOT = KeywordSlot()
CaselessKeyword =   KEYWORDSLOT(pp.CaselessKeyword)
Keyword =           KEYWORDSLOT(pp.Keyword)
Keyword("hoge")

word = pp.Forward()

preambleStatement   = pp.Forward()
bodyStatement       = pp.Forward()

setname("preambleStatement")
setname("bodyStatement")

NIheader = (
    pp.Group(preambleStatement)
    + pp.Group(bodyStatement)
    )

setaction("NIheader")

#preamble 序文の文法定義
C_comment = pp.QuotedString(
    quoteChar       = "/*",
    endQuoteChar    = "*/",
    multiline       = True
    )

preambleStatement << (
    pp.OneOrMore(
        C_comment
        )
    )


#body 本体の文法定義
word << (
    ~KEYWORDSLOT.getallkeyword()
    + pp.Regex(r"\S+")
    )

CppComment = pp.Literal("//") + pp.OneOrMore(word) + pp.LineEnd()


bodyStatement << (
    (pp.White() + bodyStatement)
    | pp.OneOrMore(
        word
        )
    )

