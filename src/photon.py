from tokens import *
from ast import *
import jast

from scanner import PhotonScanner
from compiler import Compiler

class PhotonParser(object):
    def __init__(self, scanner):
        self.scanner = scanner

    def next(self, expect = None):
        return self.scanner.next(expect)

    def peek(self):
        return self.scanner.peek()


class PhotonExpressionParser(PhotonParser):

    def nud(self, token):
        if isinstance(token, TokenLiteral):
            return IntegerLiteralExpression(token.value)
        elif isinstance(token, TokenIdentifier):
            return IdentifierExpression(token.value)

        raise SyntaxError("no nud for token '%s'" % token)

    def lbp(self, token):
        if isinstance(token, TokenOperator):
            if token.value == "+":
                return 10
            elif token.value == "*":
                return 20
            else:
                raise SyntaxError("no lbp for token: %s" % token)
        return 0

    def led(self, token, left):
        if isinstance(token, TokenOperator):
            if token.value == "+":
                right = self.parse_expression(10)
                return BinaryExpression(left, token.value, right)
            elif token.value == "*":
                right = self.parse_expression(20)
                return BinaryExpression(left, token.value, right)

        raise SyntaxError("no led for token '%s'" % token)

    def parse_expression(self, rbp = 0):
        t = self.next()
        left = self.nud(t)
        while rbp < self.lbp(self.peek()):
            t = self.peek()
            self.next()
            left = self.led(t, left)
        return left

class PhotonStatementParser(PhotonExpressionParser):
    def parse_return_statement(self):
        statement = ReturnStmt()
        self.next(Token.KEYWORD_RETURN)
        statement.expression = self.parse_expression()
        return statement

    def parse_statement(self):
        token = self.peek()
        if token == Token.KEYWORD_RETURN:
            return self.parse_return_statement()
        elif token == Token.KEYWORD_FUNCTION:
            return self.parse_function()
        else:
            self.next()
            raise SyntaxError("expected statement, got '%s'" % token)

    def parse_statement_block(self):
        self.next(Token.DELIM_LBRACE)
        statements = []
        while True:
            if self.peek() == Token.DELIM_RBRACE:
                self.next(Token.DELIM_RBRACE)
                break
            statements.append(self.parse_statement())
        return statements

    def parse_function(self):
        self.next(Token.KEYWORD_FUNCTION)
        node = FunctionStmt()
        token = self.next()
        if not token.is_identifier():
            raise SyntaxError("expected identifier, got: %s" % token)
        node.name = token.value
        node.parameters = []
        token = self.next(Token.DELIM_LPAREN)
        while True:
            token = self.next([Token.KEYWORD_INT, Token.KEYWORD_STRING])
            parameter_type = token.value
            token = self.next()
            if not token.is_identifier():
                raise SyntaxError("expected identifier, got: %s" % token)
            parameter_name = token.value
            node.parameters.append((parameter_type, parameter_name))
            token = self.next()
            if token == Token.DELIM_RPAREN:
                break
            elif token == Token.DELIM_COMMA:
                continue
            else:
                raise SyntaxError("expected ',' or ')'")
        node.statements = self.parse_statement_block()
        return node

    def parse_module(self):
        node = Module()
        statements = []
        while True:
            token = self.peek()
            if token == Token.KEYWORD_FUNCTION:
                statements.append(self.parse_function())
            elif token == Token.EOF:
                break
            else:
                raise SyntaxError(token)
        node.statements = statements
        return node

scanner = PhotonScanner('src/test.js')
parser = PhotonStatementParser(scanner)
module = parser.parse_module()

compiler = Compiler()
compiler.compile(module)

#scanner = PhotonScanner('src/expr.js')
#parser = PhotonExpressionParser(scanner)
#print parser.parse_expression()
