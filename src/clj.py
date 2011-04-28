from serializer import Serializer

python_list = list

class node(object):
    def accept(self, visitor):
        return getattr(visitor, ('visit_' + self.__class__.__name__).lower())(self)

class ident(node):
    def __init__(self, name):
        self.name = name

class intliteral(node):
    def __init__(self, value):
        self.value = value

class list(node):
    def __init__(self, elements = None):
        self.elements = python_list(elements if elements else [])

    def append(self, element):
        self.elements.append(element)

    def __iter__(self):
        return iter(self.elements)

class vector(list):
    pass

class mod(list):
    pass

class block(list):
    def __init__(self, inc, elements):
        self.inc = inc
        list.__init__(self, elements)

class PrettyPrinter(Serializer):
    def __init__(self):
        pass

    def visit_vector(self, vector):
        self.emit('[')
        self.start_list()
        for item in vector:
            self.start_item()
            item.accept(self)
            self.end_item()
        self.end_list(' ')
        self.emit(']')

    def visit_list(self, list):
        self.emit('(')
        self.start_list()
        for item in list:
            self.start_item()
            item.accept(self)
            self.end_item()
        self.end_list(' ')
        self.emit(')')

    def visit_block(self, block):
        self.inc(block.inc)
        for item in block:
            self.nl()
            item.accept(self)

    def visit_defn(self, defn):
        self.visit_list(defn)
        self.level = 0

    def visit_intliteral(self, literal):
        self.emit(literal.value)

    def visit_ident(self, ident):
        self.emit(ident.name)

    def visit_mod(self, mod):
        for item in mod:
            item.accept(self)
            self.level = 0
            self.nl()
            self.nl()

    def pretty_print(self, node):
        self.start()
        node.accept(self)
        return self.end()


DEFN = ident("defn")
DO = ident("do")

if __name__ == '__main__':
    pp = PrettyPrinter()
    f1 = list([DEFN, ident("test"), vector([ident('a'), ident('b')]),
               block(1, [list([ident('+'), ident('a'), ident('b')]),
                         list([ident('+'), ident('a'), ident('b')])])])

    f2 = list([DO] +
              [block(1, [list([ident('+'), ident('a'), ident('b')]),
                         list([ident('+'), ident('a'), ident('b')])])])

    mod = mod([f1, f2])
    print pp.pretty_print(mod)

