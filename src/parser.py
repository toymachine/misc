from pyparsing import *
from ast import *
from compiler import Compiler

def createFunctionStatement(s, l, t):
    node = FunctionStatement()
    node.name = t[0]
    node.parameters = [(None, name) for name in t[1]]
    node.statements = t[2]
    return node

def createModule(s, l, t):
    node = Module()
    node.statements = t
    return node

def createReturnStatement(s, l, t):
    node = ReturnStatement()
    node.expression = t[0]
    return node

def createIdentifierExpression(s, l, t):
    return IdentifierExpression(t[0])

def createBinaryExpression(s, l, t):
    return BinaryExpression(t[0][0], t[0][1], t[0][2])


x = """
function sum(a, b) {
    return a + b + c
}
"""

KEYWORD_FUNCTION = "function"
KEYWORD_RETURN = "return"

LPAREN = Suppress("(")
RPAREN = Suppress(")")
LBRACE = Suppress("{")
RBRACE = Suppress("}")

identifier = Word(alphas, alphanums + '_')

identifierExpression = identifier.copy()
identifierExpression.setParseAction(createIdentifierExpression)

integerLiteral = Regex(r"-?\d+")

stringLiteral = quotedString

expression = Forward()

callExpression = identifier + LPAREN + Group(Optional(delimitedList(expression))) + RPAREN

operand = (callExpression | identifierExpression | integerLiteral | stringLiteral)

expression << operatorPrecedence(operand,
    [
    (oneOf("* / %"), 2, opAssoc.LEFT, createBinaryExpression),
    (oneOf("+ -"), 2, opAssoc.LEFT, createBinaryExpression),
    ])

returnStatement = Suppress(KEYWORD_RETURN) + expression
returnStatement.setParseAction(createReturnStatement)

statement = returnStatement

block = LBRACE + Group(ZeroOrMore(statement)) + RBRACE

functionDef = Suppress(KEYWORD_FUNCTION) + identifier + LPAREN + Group(Optional(delimitedList(identifier))) + RPAREN + block
functionDef.setParseAction(createFunctionStatement)

# define grammar
module = OneOrMore(functionDef)
module.setParseAction(createModule)
module.enablePackrat()

# parse input string
print x
print "->"

module_ast = module.parseString(x)[0]
pp = PrettyPrinter()
print pp.pretty_print(module_ast)
print "->"

compiler = Compiler()
compiler.compile(module_ast)




