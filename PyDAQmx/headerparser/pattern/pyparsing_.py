﻿from pyparsing import *

from . import util

KEYWORDSLOT = util.KeywordSlot()
CaselessKeywordSlot =   KEYWORDSLOT(CaselessKeyword)
KeywordSlot         =   KEYWORDSLOT(Keyword)


#start define Keywords section
# end  define Keywords section

def OneOrMoreList(pattern):
    return Group(OneOrMore(pattern))

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


expression = word.copy()
expression.setName("expression")