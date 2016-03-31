
import pyparsing as pp

from . import pyparsing_
from . import preamble
from . import valDefineMacro

bodyStatement = pyparsing_.Forward()

NIheader = (
    preamble.statement
    + bodyStatement
    )

bodyStatement << pyparsing_.OneOrMoreList(
    valDefineMacro.statement
    | pyparsing_.word.suppress()
    )
