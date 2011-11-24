

class SyntaxError(Exception):
    pass

class Result(object):
    def __init__(self, value, start, end):
        self.value, self.start, self.end = value, start, end

    def __str__(self):
        return "<result: '%s', [%d:%d]>" % (self.value, self.start, self.end)

    def __repr__(self):
        return str(self)

class Cons(object):
    def __init__(self, head, rest, start, end):
        self.head, self.rest = head, rest
        self.start, self.end = start, end

    def __str__(self):
        return "<cons [%d:%d]: '%s' .. '%s'>" % (self.start, self.end, self.head, self.rest)

    def __repr__(self):
        return str(self)

def term(w):
    def _parser(s, i):
        if s[i:].startswith(w):
            yield Result(w, i, i + len(w))
    return _parser

def alt2(left, right):
    def _parser(s, i):
        for r in left(s, i):
            yield r
        for r in right(s, i):
            yield r
    return _parser

def cat2(left, right):
    def _parser(s, i):
        for lr in left(s, i):
            for rr in right(s, lr.end):
                yield Cons(lr, rr, i, rr.end)
    return _parser

def alt(*args):
    return reduce(alt2, args)

def cat(*args):
    return reduce(cat2, args)

#m = word("piet")
#m = alt2(term("piet"), term("piet blaat"))
#m = cat2(term("piet"), term(" blaat aap"))
#m = alt2(cat2(term("pie"), term("t blaat aap")), cat2(term("p"), term("iet blaat aap")))

#m = alt(term("piet"), term("piet bl"), term("piet blaat"))
m = cat(term("piet"), term(" bl"), term("aat"))

s = "piet blaat aap"

print list(m(s, 0))


