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

def createIntegerLiteralExpression(s, l, t):
    return IntegerLiteralExpression(t[0])

def createBinaryExpression(s, l, t):
    #only in the case of LEFT ASSOC within the same pred.level, pyparsing gives us [a,+,b,+,c]
    #instead of [[a,+,b],c]
    #the recursive function createExpr deals with this and gives back the correct form
    tokens = t[0].asList()
    def createExpr(tokens):
        if len(tokens) == 3:
            return BinaryExpression(tokens[0], tokens[1], tokens[2])
        else:
            return createExpr([BinaryExpression(tokens[0], tokens[1], tokens[2])] + tokens[3:])
    return createExpr(tokens)

def createCallExpression(s, l, t):
    node = CallExpression()
    node.name = t[0]
    node.arguments = t[1]
    return node

x = """
function sum(a, b) {
    return a + b
}

function minus(a, b) {
    return a - b * sum(a, b)
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
integerLiteral.setParseAction(createIntegerLiteralExpression)

stringLiteral = quotedString

expression = Forward()

callExpression = identifier + LPAREN + Group(Optional(delimitedList(expression))) + RPAREN
callExpression.setParseAction(createCallExpression)

operand = (callExpression | identifierExpression | integerLiteral | stringLiteral)

expression << operatorPrecedence(operand,
    [
    (oneOf("* / %"), 2, opAssoc.LEFT, createBinaryExpression),
    (oneOf("+ -"), 2, opAssoc.LEFT, createBinaryExpression),
    #(oneOf("@ !"), 2, opAssoc.RIGHT, createBinaryExpression), test for right assoc
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
#print x
#print "->"

module_ast = module.parseString(x)[0]
pp = PrettyPrinter()
#print pp.pretty_print(module_ast)
#print "->"

compiler = Compiler()
compiler.compile(module_ast)

print "(println (minus 10 20))"



