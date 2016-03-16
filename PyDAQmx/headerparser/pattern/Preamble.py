from . import pyparsing_

content = pyparsing_.cStyleComment.copy()
content.setName("<content>")

statement = pyparsing_.OneOrMore(
    content
    )