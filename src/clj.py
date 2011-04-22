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

class hint(node):
    pass

hint.INDENT = hint()

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

    def visit_intliteral(self, literal):
        self.emit(literal.value)

    def visit_ident(self, ident):
        self.emit(ident.name)

    def pretty_print(self, node):
        self.start()
        node.accept(self)
        return self.end()


DEFN = ident("defn")
DO = ident("do")



