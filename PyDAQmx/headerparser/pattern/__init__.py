
import pyparsing as pp

from . import pyparsing_
from . import preamble
from . import valDefineMacro

statements = pyparsing_.Forward()

NIheader = (
    preamble.statement
    + statements
    )

statements << pyparsing_.OneOrMore(
    valDefineMacro.statement
    | pyparsing_.word.suppress()
    )
