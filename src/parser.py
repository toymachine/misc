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

def createBindStatement(s, l, t):
    node = BindStatement()
    node.name = t[1]
    node.expr = t[2]
    return node

def createIfExpression(s, l, t):
    node = IfExpression()
    node.expr = t[0]
    node.trueBlock = t[1]
    node.falseBlock = t[2]
    return node

def createIdentifierExpression(s, l, t):
    return IdentifierExpression(t[0])

def createIntegerLiteralExpression(s, l, t):
    return IntegerLiteralExpression(t[0])

def createStringLiteralExpression(s, l, t):
    return StringLiteralExpression(t[0])

def createListLiteralExpression(s, l, t):
    return ListLiteralExpression(t)

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

def createForStatement(s, l, t):
    node = ForStatement()
    node.bind = t[0]
    node.expr = t[1]
    node.block = t[2]
    return node

KEYWORD_FUNCTION = "function"
KEYWORD_VAL = "val"
KEYWORD_RETURN = "return"
KEYWORD_IF = "if"
KEYWORD_ELSE = "else"
KEYWORD_FOR = "for"
KEYWORD_IN = "in"

LPAREN = Suppress("(")
RPAREN = Suppress(")")
LBRACE = Suppress("{")
RBRACE = Suppress("}")
LBRACK = Suppress("[")
RBRACK = Suppress("]")

identifier = Word(alphas, alphanums + '_')

identifierExpression = identifier.copy()
identifierExpression.setParseAction(createIdentifierExpression)

integerLiteral = Regex(r"-?\d+")
integerLiteral.setParseAction(createIntegerLiteralExpression)

stringLiteral = quotedString.copy()
stringLiteral.setParseAction(createStringLiteralExpression)

expression = Forward()

listLiteral = LBRACK + Optional(delimitedList(expression)) + RBRACK
listLiteral.setParseAction(createListLiteralExpression)

callExpression = identifier + LPAREN + Group(Optional(delimitedList(expression))) + RPAREN
callExpression.setParseAction(createCallExpression)

operand = (callExpression | identifierExpression | integerLiteral | stringLiteral | listLiteral)

expression << operatorPrecedence(operand,
    [
    (oneOf("* / %"), 2, opAssoc.LEFT, createBinaryExpression),
    (oneOf("+ -"), 2, opAssoc.LEFT, createBinaryExpression),
    ("==", 2, opAssoc.LEFT, createBinaryExpression),
    ])

statement = Forward()

block = LBRACE + Group(ZeroOrMore(statement)) + RBRACE

ifExpression = Suppress(KEYWORD_IF) + LPAREN + expression + RPAREN + block + Optional(Suppress(KEYWORD_ELSE) + block)
ifExpression.setParseAction(createIfExpression)

exprStatement = (ifExpression | expression)

returnStatement = Suppress(KEYWORD_RETURN) + exprStatement
returnStatement.setParseAction(createReturnStatement)

bindStatement = KEYWORD_VAL + identifier + Suppress("=") + exprStatement
bindStatement.setParseAction(createBindStatement)

forStatement = Suppress(KEYWORD_FOR) + LPAREN + identifier + Suppress(KEYWORD_IN) + expression + RPAREN + block
forStatement.setParseAction(createForStatement)

statement << (bindStatement | returnStatement | forStatement | exprStatement)

functionDef = Suppress(KEYWORD_FUNCTION) + identifier + LPAREN + Group(Optional(delimitedList(identifier))) + RPAREN + block
functionDef.setParseAction(createFunctionStatement)

# define grammar
module = OneOrMore(functionDef)
module.setParseAction(createModule)
module.enablePackrat()
module.ignore(cppStyleComment)

# parse input string
#print x
#print "->"
import sys

module_ast = module.parseString(open(sys.argv[1]).read())[0]
pp = PrettyPrinter()
#print pp.pretty_print(module_ast)
#print "->"

compiler = Compiler()
compiler.compile(module_ast)

print "(println (main 10 20))"



