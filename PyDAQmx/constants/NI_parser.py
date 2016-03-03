from . import NI_AST
import pyparsing

commentL = (pyparsing.LineStart() + pyparsing.Literal("/*"))
commentR = (pyparsing.Literal("/*") + pyparsing.LineEnd()  )


preamble = pyparsing.OneOrMore(
    (commentL + (pyparsing.Word("-")|pyparsing.Word("=")) + commentR) | commentL + pyparsing.OneOrMore(pyparsing.alphanums | pyparsing.Word("/-():.")) + commentR)
content  = pyparsing.Regex(".*") 

header = preamble + content
header.setParseAction(NI_AST.Header.handler)