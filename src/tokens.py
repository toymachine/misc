class Token(object):
    def __init__(self, value):
        self.value = value

    def is_identifier(self):
        return False

    def __repr__(self):
        return "<token '%s'>" % self.value

class TokenOperator(Token):
    pass

class TokenLiteral(Token):
    pass

class TokenIdentifier(Token):
    def is_identifier(self):
        return True

class TokenKeyword(Token):
    ALL = {}

    def __init__(self, value):
        Token.__init__(self, value)
        self.ALL[value] = self

    @classmethod
    def get(cls, value):
        return cls.ALL.get(value, None)

class TokenDelimiter(Token):
    pass

class Keyword(object):
    pass

Keyword.FUNCTION = "function"
Keyword.IF = "if"
Keyword.THEN = "then"
Keyword.ELSE = "else"
Keyword.RETURN = "return"
Keyword.BOOL = "bool"
Keyword.INT = "int"
Keyword.STRING = "string"
Keyword.VOID = "void"
Keyword.TRUE = "true"
Keyword.FALSE = "false"

#Keyword.ALL = set([Keyword.FUNCTION, Keyword.IF, Keyword.THEN, Keyword.ELSE, Keyword.RETURN,
#                   Keyword.BOOL, Keyword.INT, Keyword.STRING, Keyword.VOID, Keyword.TRUE, Keyword.FALSE])

Token.OP_PLUS = TokenOperator("+")
Token.OP_MIN = TokenOperator("-")
Token.OP_MUL = TokenOperator("*")
Token.OP_DIV = TokenOperator("/")
Token.OP_EQUALS = TokenOperator("==")
Token.OP_ASSIGN = TokenOperator("=")

Token.KEYWORD_FUNCTION = TokenKeyword(Keyword.FUNCTION)
Token.KEYWORD_IF = TokenKeyword(Keyword.IF)
Token.KEYWORD_THEN = TokenKeyword(Keyword.THEN)
Token.KEYWORD_ELSE = TokenKeyword(Keyword.ELSE)
Token.KEYWORD_RETURN = TokenKeyword(Keyword.RETURN)

Token.KEYWORD_BOOL = TokenKeyword(Keyword.BOOL)
Token.KEYWORD_INT = TokenKeyword(Keyword.INT)
Token.KEYWORD_STRING = TokenKeyword(Keyword.STRING)
#Token.KEYWORD_FLOAT = TokenKeyword("float")
#Token.KEYWORD_REF = TokenKeyword("ref")
#Token.KEYWORD_var = TokenKeyword("var")
Token.KEYWORD_VOID = TokenKeyword(Keyword.VOID)
Token.KEYWORD_TRUE = TokenKeyword(Keyword.TRUE)

Token.DELIM_COMMA = TokenDelimiter(",")
#Token.DELIM_SEMI = TokenDelimiter(";")
Token.DELIM_COLON = TokenDelimiter(":")
Token.DELIM_LPAREN = TokenDelimiter("(")
Token.DELIM_RPAREN = TokenDelimiter(")")
Token.DELIM_LBRACK = TokenDelimiter("[")
Token.DELIM_RBRACK = TokenDelimiter("[")
Token.DELIM_LBRACE = TokenDelimiter("{")
Token.DELIM_RBRACE = TokenDelimiter("}")
