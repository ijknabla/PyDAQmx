

def main():
    ConvertedLabel = {}

    from    PyDAQmx.headerparser            import  result
    import  PyDAQmx.headerparser.ast        as      ast
    import  PyDAQmx.headerparser.pattern    as      pattern

    def defineGlobal(name : str, value):
        import keyword
        if keyword.iskeyword(name) or not name.isidentifier():
            newName = "_{}".format(name)
            ConvertedLabel[newName] = name
            name = newName
        globals()[name] = value


    def valDefineMacroStatement_generator():
        for statement in result.statements:
            if isinstance(statement, ast.valDefineMacro.statement):
                yield statement


    def defineVal():
        for statement in valDefineMacroStatement_generator():
            title, contents = statement.values()
            for content in contents:
                header, definition = content.values()
                
                def header_generator():
                    for text in "".join(header).split("***"):
                        if text and not text.isspace():
                            yield text.strip()

                for headerLine in header_generator():
                    try:
                        print(parseHeader(headerLine))
                    except Exception as e:
                        import sys
                        sys.stderr.write(headerLine + "\n")
                        sys.stderr.write(str(e)+"\n")

                for definitionLine in definition:
                    try:
                        label, expression, detail   = definitionLine.values()
                    except ValueError:
                        label, expression,          = definitionLine.values()
                        detail                      = None

                    defineGlobal(label, eval(expression))

    def parseHeader(header):
        import pyparsing as pp
        "Values for the {} parameter of {}"
        a = (
            pp.Regex("Values?")
            + pp.Optional("set")
            + pp.Literal("for")
            + pp.Literal("the") 
            + pp.OneOrMore(~(pp.Literal("parameter") | pp.Literal("paramter")) + pp.Word(pp.alphanums + "_"))
            + (pp.Literal("parameter") | pp.Literal("paramter"))
            + pp.Literal("of")
            + (
                (
                    pp.Word(pp.alphanums)
                    + pp.Optional(
                        (pp.ZeroOrMore(~(pp.Literal("and") | pp.Literal("&")) + pp.Literal(",") + pp.Word(pp.alphanums)))
                        + pp.Optional((pp.Literal("and") | pp.Literal("&")) + pp.Word(pp.alphanums))
                        )
                    )
                ^ pp.OneOrMore(pp.Word(pp.alphanums))
                )
            + pp.LineEnd()
            )
        
        b = (
            pp.Regex("Values?")
            + pp.Literal("set")
            + pp.Word(pp.alphanums + "_")
            + pp.LineEnd()
            )
        
        c = (
            pp.Regex("Values?")
            + pp.Literal("set")
            + pp.Literal("for")
            + pp.OneOrMore(~pp.Literal("for") + pp.Word(pp.alphas))
            + pp.Literal("for")
            + pp.OneOrMore(pp.Word(pp.alphanums))
            + pp.LineEnd()
            )

        d = (
            pp.Word(pp.alphanums)
            + pp.OneOrMore(pp.Literal(",") + pp.Word(pp.alphanums))
            + pp.Literal("and")
            + pp.Word(pp.alphanums)
            + pp.LineEnd()
            )

        e = (
            pp.Regex("Values?")
            + pp.Literal("for")
            + pp.Word(pp.alphanums + "_")
            + pp.Optional(
                pp.Literal("and")
                + pp.Word(pp.alphanums + "_")
                )
            + pp.LineEnd()
            )

        f = (
            pp.Regex("Values?")
            + pp.Optional("set")
            + pp.Literal("for")
            + pp.Literal("the") 
            + pp.OneOrMore(~(pp.Literal("parameter") | pp.Literal("paramter")) + pp.Word(pp.alphanums + "_"))
            + (pp.Literal("parameter") | pp.Literal("paramter"))
            + pp.Literal("-")
            + pp.OneOrMore(pp.Word(pp.alphanums))
            )

        g = pp.Literal("/")

        #c = pp
        return (a^b^c^d^e^f^g).parseString(header)
       
    def defineCopyright():
        import re
        copyright_year = 2013
        for preambleLine in result.preamble:
            if "Copyright" in preambleLine:
                copyright_year = max(list(map(int, re.findall('\d\d\d\d', preambleLine))))

        defineGlobal("copyright_year", copyright_year)

    defineVal()
    defineCopyright()


main()
del main