from . import pyparsing_
from . import pyparsing_ as pp
from . import util

macroLabel  = pyparsing_.identifier
defineMacro = pyparsing_.Keyword("#define")


label = pyparsing_.Combine(
    pyparsing_.Literal("DAQmx_Val_").suppress()
    + pyparsing_.identifier
    )
label.setName("<DAQmx_Val_{lavel}>")

titleLine = pyparsing_.cStyleComment.copy()
titleLine.setName("<title line>")

title = pyparsing_.OneOrMore(titleLine)

headerline = pyparsing_.cppStyleCommentOnly.copy()
headerline.setName("<header line>")

header = pyparsing_.OneOrMore(headerline)

detail = pyparsing_.cppStyleCommentOnly.copy()
detail.setName("<definition detail>")

defineMacro = pyparsing_.Literal("#define").suppress()
defineMacro.setName("<define macro>")

definitionLine = pyparsing_.And([
    defineMacro,
    label,
    pyparsing_.expression,
    detail
    ])

definition = pyparsing_.OneOrMore(
    definitionLine
    )

content = (
    header
    + definition
    )

contents = pyparsing_.OneOrMore(content)

statement = (
    title
    + contents
    )