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
            return token.value

        raise SyntaxError("no nud for token '%s'" % token)

    def lbp(self, token):
        if isinstance(token, TokenOperator):
            if token.value == "+":
                return 10

        raise SyntaxError("no lbp for token '%s'" % token)

    def led(self, token, left):
        raise SyntaxError("no led for token '%s'" % token)

    def parse_expression(self, rbp = 0):
        current_token = self.next()
        next_token = self.peek()
        #print 'x', current_token, next_token
        left = self.nud(current_token)
        while rbp < self.lbp(next_token):
            current_token = next_token
            next_token = self.next()
            left = self.led(current_token, left)
        return left

class PhotonStatementParser(PhotonExpressionParser):
    def parse_return_statement(self):
        token = self.next(Token.KEYWORD_RETURN)

    def parse_statement(self):
        token = self.peek()
        if token == Token.KEYWORD_RETURN:
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
parser.parse_expression()
