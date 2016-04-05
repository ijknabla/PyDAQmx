from . import pyparsing_

content = pyparsing_.cStyleComment.copy()

statement = pyparsing_.OneOrMore(
    content
    )