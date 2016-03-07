from . import NI_AST
import pyparsing as pp

import functools, operator

def simple_QuotedString(start, end):
    return pp.QuotedString(
        quoteChar       = start,
        endQuoteChar    = end,
        multiline       = True
    )

class KeywordSlot:
    def __init__(self):
        self.allkeyword = set()

    def __call__(self, cls):
        __init__ = cls.__init__
        #@functools.wraps(__init__)
        def wrapped(*args, **kwrds):
            self.allkeyword.add(args[0])
            __init__(*args, **kwrds)
        cls.__init__ = wrapped
        print(cls.__init__)

KEYWORDSLOT = KeywordSlot()
KEYWORDSLOT(pp.CaselessKeyword)
KEYWORDSLOT(pp.Keyword)

def getallkeyword(keywordslot = KEYWORDSLOT):
    return functools.reduce(operator.or_, keywordslot.allkeyword)

#CおよびC++スタイルのコメントアウトの定義
C_comment = pp.QuotedString(
    quoteChar       = "/*",
    endQuoteChar    = "*/",
    multiline       = True
    )

Cpp_comment = \
            pp.Suppress("//")\
            + pp.Regex(".*")\
            + pp.Suppress(pp.LineEnd())

comment = C_comment | Cpp_comment

#複数のコメントアウト
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
    ifndefMacro + macroLabel
    + code
    + endifMacro
    )

ifMacroStatement = (
    ifMacro + code
    + code
    + endifMacro
    )
"""
defineMacroStatement = (
    defineMacro + macroLabel + pp.Optional(code)
    )

pragmaMacroStatement = (
    pragmaMacro + macroLabel
    )
"""

macroStatement = (
    ifdefMacroStatement
    | ifndefMacroStatement
    | ifMacroStatement
#    | defineMacroStatement
#    | pragmaMacroStatement
    )



word = ~getallkeyword() + pp.Word('#!"&\'()*+,-./:;<=[\\]^_{|}' + pp.alphanums)


code << (pp.ZeroOrMore(macroStatement | word))

preamble = C_comments

NI_header = preamble + code