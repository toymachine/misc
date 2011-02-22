from plex import *
from tokens import *

letter = Range("AZaz")
digit = Range("09")
name = letter + Rep(letter | digit)
number = Rep1(digit)

def token_or_identifier(scanner, txt):
    token = TokenKeyword.get(txt)
    if token is None:
        return TokenIdentifier(txt)
    else:
        return token

lexicon = Lexicon([
    (name,            token_or_identifier),
    (number,          'int'),
    (Str('('), Token.DELIM_LPAREN),
    (Str(')'), Token.DELIM_RPAREN),
    (Str('['), Token.DELIM_LBRACK),
    (Str(']'), Token.DELIM_RBRACK),
    (Str('{'), Token.DELIM_LBRACE),
    (Str('}'), Token.DELIM_RBRACE),
    (Str(','), Token.DELIM_COMMA),
    (Str(':'), Token.DELIM_COLON),
    (Str('+'), Token.OP_PLUS),
    (Str('-'), Token.OP_MIN),
    (Rep1(Any(" \t\n")), IGNORE)
])

class PhotonScanner(Scanner):
    def __init__(self, filename):
        f = open(filename, "r")
        Scanner.__init__(self, lexicon, f, filename)

    def next(self, expect = None):
        token, _ = self.read()
        if expect:
            if isinstance(expect, list):
                if token not in expect:
                    raise SyntaxError("expected one of: %s, but found: %s instead" % (expect, token))
            else:
                if expect is not token:
                    raise SyntaxError("expected token: %s, but found: %s instead" % (expect, token))
        return token


