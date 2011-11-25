

class SyntaxError(Exception):
    pass

class Result(object):
    def __init__(self, value, start, end):
        self.value, self.start, self.end = value, start, end

    def __str__(self):
        return "<result: '%s', [%d:%d]>" % (self.value, self.start, self.end)

    def __repr__(self):
        return str(self)

class Empty(object):
    def __init__(self, i):
        self.start = i
        self.end = i

    def __repr__(self):
        return "<empty: [%d]>" % self.start

class Cons(object):
    def __init__(self, head, rest, start, end):
        self.head, self.rest = head, rest
        self.start, self.end = start, end

    def __str__(self):
        return "<cons [%d:%d]: '%s' .. '%s'>" % (self.start, self.end, self.head, self.rest)

    def __repr__(self):
        return str(self)

def term(w):
    def parser(s, i):
        if s[i:].startswith(w):
            yield Result(w, i, i + len(w))
    return parser

def _empty():
    def parser(s, i):
        yield Empty(i)
    return parser
empty = _empty()

def eat_space(p):
    def parser(s, i):
        while i < len(s) and s[i].isspace():
            i += 1
        for r in p(s, i):
            yield r
    return parser

def token(w):
    return eat_space(term(w))

def alt2(left, right):
    def parser(s, i):
        for r in left(s, i):
            yield r
        for r in right(s, i):
            yield r
    return parser

def cat2(left, right):
    def parser(s, i):
        for lr in left(s, i):
            for rr in right(s, lr.end):
                yield Cons(lr, rr, i, rr.end)
    return parser

def alt(*args):
    return reduce(alt2, args)

def cat(*args):
    return reduce(cat2, args)


def delay(f, p):
    def parser(s, i):
        _p = f(p)
        for r in _p(s, i):
            yield r
    return parser

def one_or_more(p):
    return cat2(p, alt2(empty, delay(one_or_more, p)))
                
def zero_or_one(p):
    return alt2(empty, p)

def zero_or_more(p):
    return alt2(empty, one_or_more(p))

#whitespace
#syntaxerror


