import PyDAQmx
import PyDAQmx.headerparser.ast as ast

def print_key(obj):
    if isinstance(obj, dict):
        print(set(obj.keys()))
    else:
        print("list")

for statement in PyDAQmx.headerparser.result.body:
    if isinstance(statement, ast.valDefineMacro.statement):
        #print(statement.title)
        for content in statement.contents:
            header      = content.header
            definition  = content.definition
            print("\n".join((" ".join(header).split("***"))))
            print("==========")
            