

def main():
    ConvertedLabel = {}

    import keyword, re
    import PyDAQmx
    import PyDAQmx.headerparser.ast as ast
    import PyDAQmx.headerparser.pattern as pattern

    def print_key(obj):
        if isinstance(obj, dict):
            print(set(obj.keys()))
        else:
            print("list")

    for statement in PyDAQmx.headerparser.result.statements:

        if isinstance(statement, ast.valDefineMacro.statement):
            valDefineMacro = statement
            for content in statement.contents:
                header      = content.header
                definition  = content.definition
                for definitionLine in content.definition:
                    label       = definitionLine.label
                    expression  = definitionLine.expression

                    if keyword.iskeyword(label) or not label.isidentifier():
                        ConvertedLabel[label] = "_" + label
                        label = ConvertedLabel[label]

                    value = eval(expression)
                    
                    
                    if "detail" in definitionLine:
                        pass

                    globals()[label] = value

    copyright_year = 2013
    for preambleLine in PyDAQmx.headerparser.result.preamble:
        if "Copyright" in preambleLine:
            copyright_year = max(list(map(int, re.findall('\d\d\d\d', preambleLine))))       
    globals()["copyright_year"] = copyright_year



main()
del main