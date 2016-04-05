
import pyparsing as pp

from . import pyparsing_
from . import preamble
from . import valDefineMacro

bodyStatements = pyparsing_.Forward()

NIheader = (
    preamble.statement
    + bodyStatements
    )

bodyStatements << pyparsing_.OneOrMore(
    valDefineMacro.statement
    | pyparsing_.word.suppress()
    )
