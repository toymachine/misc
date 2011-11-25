

def term(w):
    def parser(s, i):
        if s[i:].startswith(w):
            yield (w, i, i + len(w))
    return parser

def alt2(left, right):
    def parser(s, i):
        for r in left(s, i):
            yield r
        for r in right(s, i):
            yield r
    return parser

def cat2(left, right):
    def parser(s, i):
        for lval, lstart, lend in left(s, i):
            for rval, rstart, rend in right(s, lend):
                yield ((lval, rval), i, rend)
    return parser

def empty(s, i):
    yield ("<empty>", i, i)

def zero_or_one(p):
    return alt2(empty, p)

def delay(f, p):
    def parser(s, i):
        _p = f(p)
        for r in _p(s, i):
            yield r
    return parser

def one_or_more(p):
    return cat2(p, alt2(empty, delay(one_or_more, p)))
                
def zero_or_more(p):
    return alt2(empty, one_or_more(p))



def alt(*args):
    return reduce(alt2, args)

def cat(*args):
    return reduce(cat2, args)

def eof(s, i):
    if i == len(s):
        yield ("<eof>", i, i)


