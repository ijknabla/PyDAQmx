""" Initialize the constants from the NIDAQmx.h file

Read the NIDAQmx.h file and "execute" the #define command
"""



"""
class Preamble(pyparsing.Group):pass
preamble = pyparsing.OneOrMore(comment)
expression = pyparsing.Empty()

NIDAQmxheader = Preamble(pyparsing.OneOrMore(comment))

result = NIDAQmxheader.parseFile(DAQmxConfig.dot_h_file)

include_file = open(DAQmxConfig.dot_h_file,'r') #Open NIDAQmx.h file

# Try get the version of NIDAQmx
preamble = []
for line in include_file:
    if line.startswith('/*'):
        preamble.append(line)
    else:
        break

for copyright_line in preamble:
    if "Copyright" in copyright_line:
        DAQmx_copyright_year = max(list(map(int, re.findall('\d\d\d\d', copyright_line))))
        break
else:
    DAQmx_copyright_year = 2003

# Regular expression to parse the #define line
# Parse line like : #define PI 3.141592
# The first group is the name of the constant
# The second group the value
define = re.compile(r'\#define\s+(\S+)\s+(".*"|\S+)')

#空白行のパターン
space  = re.compile(r"\s*$") 

#ifマクロの認識
ifmacro  = re.compile(r"(#ifdef|#ifndef|#if)")
endif         = re.compile(r"#endif")

def split2section(stream):
    ifmacro_depth = 0
    section = []
    for n, line in enumerate(stream):
        if space.match(line):
            if ifmacro_depth == 0 and section:
                yield section
                section = []
        else:
            if ifmacro.match(line):
                print(n, line)
                ifmacro_depth += 1
            elif endif.match(line):
                print(n, line)
                ifmacro_depth -= 1
            section.append(line.strip())
    if ifmacro_depth == 0 and section:
        yield section

result = list(split2section(include_file))

# List containing all the name of the constant
constant_list = []

for line in include_file:
    m = define.match(line)
    if m:
        name = m.group(1)
        value = m.group(2)
        try:
            exec(name+'='+value)
        except NameError:
            pass
        except SyntaxError:
            pass
        else:
            constant_list.append(name)

include_file.close()
"""