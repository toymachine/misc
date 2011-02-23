from serializer import Serializer

class Node(object):
    def __accept__(self, visitor):
        return getattr(visitor, 'visit' + self.__class__.__name__)(self)

class Module(Node):
    pass

class Statement(Node):
    pass

class Expression(Node):
    pass

class FunctionStmt(Statement):
    pass

class ReturnStmt(Statement):
    pass

class BinaryExpression(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class IdentifierExpression(Expression):
    def __init__(self, identifier):
        self.identifier = identifier

class IntegerLiteralExpression(Expression):
    def __init__(self, value):
        self.value = value

class PrettyPrinter(Serializer):
    def __init__(self):
        Serializer.__init__(self)

    def visitModule(self, module):
        for statement in module.statements:
            statement.__accept__(self)

    def visitIntegerLiteralExpression(self, integer_literal_expression):
        self.emit(integer_literal_expression.value)

    def visitIdentifierExpression(self, identifier_expression):
        self.emit(identifier_expression.identifier)

    def visitBinaryExpression(self, binary_expression):
        self.emit('(')
        binary_expression.left.__accept__(self)
        self.emit(binary_expression.operator)
        binary_expression.right.__accept__(self)
        self.emit(')')

    def visitReturnStmt(self, return_statement):
        self.emit("return ")
        return_statement.expression.__accept__(self)

    def visitFunctionStmt(self, function_statement):
        self.emit("function " + function_statement.name + "(")
        self.start_list()
        for arg_type, arg_name in function_statement.arguments:
            self.start_item()
            self.emit(arg_type + " "  + arg_name)
            self.end_item()
        self.end_list()
        self.emit(")")
        self.nl()
        self.emit('{')
        self.inc()
        self.nl()
        for statement in function_statement.statements:
            statement.__accept__(self)
        self.dec()
        self.nl()
        self.emit("}")
        self.nl()
        self.nl()

    def pretty_print(self, node):
        self.start()
        node.__accept__(self)
        return self.end()

