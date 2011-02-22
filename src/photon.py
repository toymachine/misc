from tokens import *

from scanner import PhotonScanner

class PhotonParser(object):
    def __init__(self, scanner):
        self.scanner = scanner

    def next(self, expect = None):
        return self.scanner.next(expect)

    def parse_statement_block(self):
        token = self.next(Token.DELIM_LBRACE)
        token = self.next(Token.DELIM_RBRACE)

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

scanner = PhotonScanner('src/test.js')
parser = PhotonParser(scanner)
parser.parse_module()

