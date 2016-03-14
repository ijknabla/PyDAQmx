from . import AST
import pyparsing as pp

import functools, operator

def setaction(name):
    target = globals()[name]
    target.setParseAction(getattr(AST, name))

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

bodyStatement = pp.Forward()
"""
bodyStatement << pp.OneOrMore(
    CppComment
    | word
    )
"""
bodyStatement << (
    (pp.White() + bodyStatement)
    | pp.OneOrMore(
        word
        )
    )

"""
#C¨æÑC++X^CÌRgAEgÌè`

Cpp_comment = \
            pp.Suppress("//")\
            + pp.Regex(".*")\
            + pp.Suppress(pp.LineEnd())

comment = C_comment | Cpp_comment

#¡ÌRgAEg
C_comments      = pp.ZeroOrMore(C_comment)
Cpp_comments    = pp.ZeroOrMore(Cpp_comment)
comments        = pp.ZeroOrMore(comment)

code = pp.Forward()
macroLabel = pp.Word(pp.alphas + "_")

endifMacro  = pp.CaselessKeyword("#endif")

ifdefMacro  = pp.CaselessKeyword("#ifdef")
ifndefMacro = pp.CaselessKeyword("#ifndef")
ifMacro     = pp.CaselessKeyword("#if")
#defineMacro = pp.CaselessKeyword("#define")
#pragmaMacro = pp.CaselessKeyword("#pragma")

ifdefMacroStatement = (
    ifdefMacro + macroLabel
    + code
    + endifMacro
    )

ifndefMacroStatement = (
    pp.Suppress(ifndefMacro) + macroLabel
    + pp.Group(code)
    + pp.Suppress(endifMacro)
    )
#ifndefMacroStatement.setParseAction(NI_AST.ifndefMacroStatement)

ifMacroStatement = (
    ifMacro + code
    + code
    + endifMacro
    )

defineMacroStatement = (
    defineMacro + macroLabel + pp.Optional(code)
    )

pragmaMacroStatement = (
    pragmaMacro + macroLabel
    )


macroStatement = (
    ifdefMacroStatement
    | ifndefMacroStatement
    | ifMacroStatement
#    | defineMacroStatement
#    | pragmaMacroStatement
    )



word << (
    ~getallkeyword() + pp.Word('#!"&\'()*+,-./:;<=[\\]^_{|}' + pp.alphanums)


code << pp.ZeroOrMore(macroStatement | word)

preamble = C_comments

NI_header = preamble + code
"""