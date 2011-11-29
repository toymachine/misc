import re

from comb import *

def skip_space(s, i):
    while i < len(s) and s[i].isspace():
        i += 1
    return i
    
def eat_space(p):
    def parser(s, i):
        i = skip_space(s, i)
        for r in p(s, i):
            yield r
    return parser

def token(w):
    return eat_space(term(w))


def _integer_literal():
    RE_INTEGER_LITERAL = re.compile(r"\d+")
    def parser(s, i):
        match = RE_INTEGER_LITERAL.match(s, i)
        if match:
            yield (match.group(), match.start(), match.end())
    return eat_space(parser)

integer_literal = _integer_literal()

def precedence_climber(primary, operators = None):
    operators = operators or \
        [('+', "bla"),
         ('-', "piet")]

    def next_token(s, i):
        i = skip_space(s, i)
        for operator in operators:
            if s[i:].startswith(operator[0]):
                return operator
        assert False, 'unknown operator from: %s' % s[i:]

    def parse_expression(lhs, min_precedence, s, i):
        op = next_token(s, i)
        print 'op', op

    def parser(s, i):
        val, start, end = list(primary(s, i))[0]
        parse_expression(val, 0, s, end)

    return parser

class forward(object):
    def __init__(self):
        self.p = None

    def define(self, p):
        self.p = p

    def __call__(self, s, i):
        for r in self.p(s, i):
            yield r

#m = word("piet")
#m = alt2(term("piet"), term("piet blaat"))
#m = cat2(term("piet"), term(" blaat aap"))
#m = alt2(cat2(term("pie"), term("t blaat aap")), cat2(term("p"), term("iet blaat aap")))

#m = alt(term("piet"), term("piet bl"), term("piet blaat"))

def printres(res):
    for x in res:
        print x

def x1():
    m = cat(term("piet"), term(" bl"), term("aat"))
    s = "piet blaat aap"
    print list(m(s, 0))

def x2():
    m = zero_or_more(term("a"))

    s = "aaa"

    printres(m(s, 0))

def x4():
    m = cat(term("a"), term("b"), term("a"))

    s = "abab"

    printres(m(s, 0))

def x3():
    s = """
namespace   {

function() {

}

}"""

    NAMESPACE = token("namespace")
    FUNCTION = token("function")
    LBRACE = token("{")
    RBRACE = token("}")
    LPAREN = token("(")
    RPAREN = token(")")

    function_stmt = cat(FUNCTION, LPAREN, RPAREN, LBRACE, RBRACE)

    stmts = zero_or_more(function_stmt)
    
    module = cat(NAMESPACE, LBRACE, stmts, RBRACE, eof)

    expression = forward()

    primary = alt( cat(LPAREN, expression, RPAREN), 
                   integer_literal)

    expression.define( precedence_climber(primary) )

    printres(module(s, 0))

    printres(expression("1 += 2", 0))

x3()

def x5():
    s = """10"""

    
printres(integer_literal("123", 0))
