
import pyparsing as pp

import functools, operator

def setname(name):
    if not isinstance(name, str):raise TypeError
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

word = pp.Forward()
identifier = pp.Forward()
setname("word")
setname("identifier")

preambleStatement   = pp.Forward()
bodyStatement       = pp.Forward()

setname("preambleStatement")
setname("bodyStatement")

NIheader = (
    pp.Group(preambleStatement)
    + pp.Group(bodyStatement)
    )



#preamble 序文の文法定義
preambleContent = pp.cStyleComment.copy()

preambleStatement << (
    pp.OneOrMore(
        preambleContent
        )
    )

expression = pp.Forward()
expression = (
    word
    )
setname("expression")

#マクロ関連の文法定義
macroLabel = identifier
defineMacro = Keyword("#define")

defineMacroStatement_nonval = (
    pp.Suppress(defineMacro)
    + macroLabel
    )

defineMacroStatement_val = (
    pp.Suppress(defineMacro)
    + macroLabel
    + expression
    )


defineMacroStatement = (
    defineMacroStatement_nonval
    | defineMacroStatement_val
    )

ValDefineMacroLabel = pp.Combine(
    pp.Literal("DAQmx_Val_").suppress()
    + identifier
    )
setname("ValDefineMacroLabel")

ValDefineMacroTitle = pp.cppStyleComment.copy()
setname("ValDefineMacroTitle")


ValDefineMacroContent = (
    pp.Suppress(defineMacro)
    + ValDefineMacroLabel
    + expression
    + pp.cppStyleComment
    )

ValDefineMacroStatement = (
    pp.Group(pp.OneOrMore(ValDefineMacroTitle))
    + pp.Group(pp.OneOrMore(ValDefineMacroContent))
    )


bodyStatement << pp.OneOrMore(
    ValDefineMacroStatement | word.suppress()
    )

#最後に定義しないといけないやつら
word << (
#    ~KEYWORDSLOT.getallkeyword()
    pp.Regex(r"\S+")
    )

identifier << (
    ~KEYWORDSLOT.getallkeyword()
    + pp.Word(pp.alphas + "_", pp.alphanums + "_")
    )