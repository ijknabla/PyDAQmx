
import pyparsing as pp

from . import pyparsing_
from . import Preamble
from . import ValDefineMacro

bodyStatement = pyparsing_.Forward()

NIheader = (
    Preamble.statement
    + bodyStatement
    )

bodyStatement << pyparsing_.Group(
    pyparsing_.OneOrMore(
        ValDefineMacro.statement
        | pyparsing_.word.suppress()
        )
    )
