from pyparsing import *

data = open("code.q","r")

LBRACE,RBRACE,LPAREN,RPAREN,SEMI,EQUAL = map(Suppress,"{}();=")
GROUP = Keyword("group")
ENTRY = Keyword("enter")
PRINT = Keyword("print")
VAR = Keyword("local")
FROM = Keyword("from")

real = Regex(r"[+-]?\d+\.\d*").setParseAction(lambda t:float(t[0]))
integer = Regex(r"[+-]?\d+").setParseAction(lambda t:int(t[0]))

# parses a string enclosed in quotes, but strips off the quotes at parse time
string = QuotedString('"')

# define structure expressions
value = string | real | integer
entry = Group(ENTRY + LPAREN + Group(Optional(delimitedList(value)))) + RPAREN + SEMI

# define print function
value = string | real | integer
print = Group(PRINT + LPAREN + string("content") + RPAREN + SEMI

# since Groups can contain Groups, need to use a Forward to define recursive expression
group = Forward()
group << Group(GROUP + LPAREN + string("name") + RPAREN + 
            LBRACE + Group(ZeroOrMore(group | entry))("body") + RBRACE)
              
# define variables
value = string | real | integer
var = Group(VAR + " " + string("var_name") + EQUAL + Group(Optional(delimitedList(value)))) + SEMI)

# define from
from = Forward()
from << Group(FROM + " " + string("module") + SEMI)

# ignore C style comments wherever they occur
group.ignore(cStyleComment)

# parse the sample text
result = group.parseString(data)

# print out the tokens as a nice indented list using pprint
from pprint import pprint
pprint(result.asList())
