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

def alt_tokens(*ws):
    return alt(*map(token, ws))

def longest(p):
    def parser(s, i):
        longest_len = -1
        longest_res = None
        for val, start, end in p(s, i):
            l = end - start
            if l > longest_len:
                longest_res = (val, start, end)
        if longest_res:
            yield longest_res
    return parser

def _integer_literal():
    RE_INTEGER_LITERAL = re.compile(r"\d+")
    def parser(s, i):
        match = RE_INTEGER_LITERAL.match(s, i)
        if match:
            yield (match.group(), match.start(), match.end())
    return eat_space(parser)

integer_literal = _integer_literal()

def precedence_climber(primary, operators = None):
    class EOF(Exception): pass

    operators = operators or \
        [('*', 2),
         ('+', 1),
         ('-', 1),
         ('+=', 1)]
        
    operator_map = dict([(x[0], x) for x in operators])
    operator_parser = longest(alt_tokens(*[x[0] for x in operators]))

    def next_token(s, i):
        print 'next tok', repr(s[i:])
        if i >= len(s):
            raise EOF()
        res = list(operator_parser(s, i))
        assert len(res) == 1, "expected to find exactly one operator: + " + repr(res)
        operator, start, end = res[0]
        return operator_map[operator], end

    def parse_primary(s, i):
        print 'prs prim', i, repr(s[i:])
        r = list(primary(s, i))[0]
        print 'prs prim res', int(r[0])
        return int(r[0]), r[2]

    def parse_expression(lhs, min_precedence, s, i):
        print 'parseexp', repr(lhs), min_precedence, repr(s[i:])
        while True:
            try:
                (op, op_precedence), i = next_token(s, i)
                print '1a op', repr(op), op_precedence
            except EOF:
                print '1b', 'EOF'
                break
            if op_precedence < min_precedence:
                print '1c', op_precedence < min_precedence
                break
            rhs, i = parse_primary(s, i)
            print 'pp result', repr(rhs), 'rest', repr(s[i:])
            #print op, i, s[i:], rhs
            while True:
                try:
                    (la_op, la_precedence), i = next_token(s, i)
                    print '2a, la', repr(la_op), la_precedence
                except EOF:
                    break
                if not la_precedence >= op_precedence:
                    break
                rhs, i = parse_expression(rhs, la_precedence, s, i)
            print lhs, op, rhs
        #print 'ret'

    def parser(s, i):
        lhs, i = parse_primary(s, i)
        yield parse_expression(lhs, 0, s, i)

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
    print 'res:'
    for i, x in enumerate(res):
        print i, x

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
    
    #printres(module(s, 0))

    printres(expression("2 + 3 * 4 + 5", 0))

x3()

def x5():
    s = """10"""

    
#printres(integer_literal("123", 0))
#printres(longest(alt_tokens("+", "-", "+="))(" +=", 0))
