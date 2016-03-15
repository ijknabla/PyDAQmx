from . import pyparsing_
from . import pyparsing_ as pp
from . import util

macroLabel  = pyparsing_.identifier
defineMacro = pyparsing_.Keyword("#define")


ValDefineMacroLabel = pyparsing_.Combine(
    pyparsing_.Literal("DAQmx_Val_").suppress()
    + pyparsing_.identifier
    )

ValDefineMacroTitle = pyparsing_.Group(
    pyparsing_.OneOrMore(pyparsing_.cStyleComment.copy())
    )

ValDefineMacroHeaderline = pyparsing_.cppStyleCommentOnly.copy()


ValDefineMacroHeader = pyparsing_.Group(
    pyparsing_.OneOrMore(ValDefineMacroHeaderline)
    )


ValDefineMacroContent = (
    pyparsing_.Literal("#define").suppress()
    + macroLabel
    + pyparsing_.expression
    + pyparsing_.cppStyleCommentOnly
    )

ValDefineMacroContents = pyparsing_.Group(
    pyparsing_.OneOrMore(ValDefineMacroContent)
    )

statement = (
    ValDefineMacroTitle
    + ValDefineMacroContents
    )