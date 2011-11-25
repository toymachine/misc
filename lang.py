from comb import *

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

def x3():
    s = """
namespace   {

function() {

}

}
"""

    NAMESPACE = token("namespace")
    FUNCTION = token("function")
    LBRACE = token("{")
    RBRACE = token("}")
    LPAREN = token("(")
    RPAREN = token(")")

    function_stmt = cat(FUNCTION, LPAREN, RPAREN, LBRACE, RBRACE)

    stmts = zero_or_more(function_stmt)
    
    module = cat(NAMESPACE, LBRACE, stmts, RBRACE)
    
    printres(module(s, 0))

x3()
