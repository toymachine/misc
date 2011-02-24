from tokens import *

from scanner import PhotonScanner

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
            return token
        elif isinstance(token, TokenIdentifier):
            return token
        raise SyntaxError("no nud for token '%s'" % token)

    def lbp(self, token):
        if isinstance(token, TokenOperator):
            if token.value == "+":
                return 10
        elif token == Token.EOF:
            return 0

        raise SyntaxError("no lbp for token '%s'" % token)

    def led(self, token, left):
        if isinstance(token, TokenOperator):
            if token.value == "+":
                right = self.parse_expression(10)
                return (left, token.value, right)

        raise SyntaxError("no led for token '%s'" % token)

    def parse_expression(self, rbp = 0):
        t = self.next()
        #print 'x', t, self.peek()
        #print 'nud of', t
        left = self.nud(t)
        #print 'lbp of token', self.peek()
        while rbp < self.lbp(self.peek()):
            t = self.peek()
            self.next()
            #print 'y', t, self.peek()
            #print 'led of t', t
            left = self.led(t, left)
            #print 'rbp, token, lbp', rbp, self.peek(), self.lbp(self.peek())
        #print 'ret left'
        return left

class PhotonStatementParser(PhotonExpressionParser):
    def parse_return_statement(self):
        token = self.next(Token.KEYWORD_RETURN)
        expr = self.parse_expression()
        print 'expr'

    def parse_statement(self):
        token = self.peek()
        print 'ps', token
        if token == Token.KEYWORD_RETURN:
            print 'parse ret'
            self.parse_return_statement()
        else:
            self.next()
            raise SyntaxError("expected statement, got '%s'" % token)

    def parse_statement_block(self):
        token = self.next(Token.DELIM_LBRACE)
        while True:
            if self.peek() == Token.DELIM_RBRACE:
                self.next(Token.DELIM_RBRACE)
                break
            self.parse_statement()

    def parse_function(self):
        token = self.next()
        if not token.is_identifier():
            raise SyntaxError("expected identifier")
        token = self.next(Token.DELIM_LPAREN)
        while True:
            token = self.next([Token.KEYWORD_INT, Token.KEYWORD_STRING])
            token = self.next()
            if not token.is_identifier():
                raise SyntaxError("expected identifier")
            token = self.next()
            if token == Token.DELIM_RPAREN:
                break
            elif token == Token.DELIM_COMMA:
                continue
            else:
                raise SyntaxError("expected ',' or ')'")
        self.parse_statement_block()

    def parse_module(self):
        while True:
            token = self.next()
            if token == Token.KEYWORD_FUNCTION:
                self.parse_function()
            elif token is None:
                break
            else:
                raise SyntaxError()

#scanner = PhotonScanner('src/test.js')
#parser = PhotonStatementParser(scanner)
#parser.parse_module()

scanner = PhotonScanner('src/expr.js')
parser = PhotonExpressionParser(scanner)
print parser.parse_expression()
