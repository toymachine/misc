class extent(object):
    def __init__(self, s, start = 0, end = None):
        self.s, self.start, self.end = s, start, len(s) if end is None else end

    def __add__(self, other):
        assert False

    def startswith(self, prefix):
        return self.s[self.start:self.end].startswith(prefix)
    
    def __getitem__(self, index):
        return extent(self.s, 
                      index.start if index.start is not None else self.start, 
                      index.stop if index.stop is not None else self.end)

def term(w):
    def parser(e):
        if e.startswith(w):
            yield (w, e[:len(w)])
    return parser

def alt2(left, right):
    def parser(e):
        for r in left(e):
            yield r
        for r in right(e):
            yield r
    return parser

def cat2(left, right):
    def parser(e):
        for left_val, left_extent in left(e):
            for right_val, right_extent in right(e[left_extent.end:]):
                yield ((left_val, right_val), e[:right_extent.end])
    return parser

def empty(e):
    yield ("<empty>", e[0:0])

def zero_or_one(p):
    return alt2(empty, p)

def delay(f, p):
    def parser(e):
        _p = f(p)
        for r in _p(e):
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
        yield ("<eof>", e[0:0])


