from pyparsing import *

from . import util

KEYWORDSLOT = util.KeywordSlot()
CaselessKeywordSlot =   KEYWORDSLOT(CaselessKeyword)
KeywordSlot         =   KEYWORDSLOT(Keyword)


#start define Keywords section
# end  define Keywords section


cppStyleCommentOnly = (
    ~cStyleComment
    + cppStyleComment
    )
cppStyleCommentOnly.setName(
    '"// C++ Style Comment $"'
    )


word = (
    ~KEYWORDSLOT.getallkeyword()
    + Regex("\S+")
    )
word.setName("word")


identifier = (
    ~KEYWORDSLOT.getallkeyword()
    + Word(
        (alphas    + "_"),
        (alphanums + "_")
        )
    )
identifier.setName("identifier")


expression = (
    word
    )
expression.setName("expression")