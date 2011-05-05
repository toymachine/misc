from serializer import Serializer

class Node(object):
    def accept(self, visitor):
        return getattr(visitor, 'visit_' + self.__class__.__name__)(self)

class Module(Node):
    pass

class Statement(Node):
    pass

class Expression(Node):
    pass

class FunctionStatement(Statement):
    def __init__(self):
        self.name = ""
        self.statements = []

class ReturnStatement(Statement):
    pass

class BindStatement(Statement):
    pass

class CallExpression(Expression):
    def __init__(self):
        self.name = ""
        self.arguments = []

class IfExpression(Expression):
    pass

class BinaryExpression(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class IdentifierExpression(Expression):
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return "<ast.ident '%s'>" % self.identifier

class IntegerLiteralExpression(Expression):
    def __init__(self, value):
        self.value = value

class StringLiteralExpression(Expression):
    def __init__(self, value):
        self.value = value

class PrettyPrinter(Serializer):
    def __init__(self):
        Serializer.__init__(self)

    def visit_Module(self, module):
        for statement in module.statements:
            statement.accept(self)

    def visit_IntegerLiteralExpression(self, integer_literal_expression):
        self.emit(integer_literal_expression.value)

    def visit_StringLiteralExpression(self, literal_expression):
        self.emit(literal_expression.value)

    def visit_IdentifierExpression(self, identifier_expression):
        self.emit(identifier_expression.identifier)

    def visit_BinaryExpression(self, binary_expression):
        self.emit('(')
        binary_expression.left.accept(self)
        self.emit(binary_expression.operator)
        binary_expression.right.accept(self)
        self.emit(')')

    def visit_IfExpression(self, if_expression):
        self.emit('if(')
        if_expression.expr.accept(self)
        self.emit(')')
        self.emitBlock(if_expression.trueBlock)
        self.emit("else")
        self.emitBlock(if_expression.falseBlock)

    def visit_ReturnStatement(self, return_statement):
        self.emit("return ")
        return_statement.expression.accept(self)

    def visit_BindStatement(self, bind_statement):
        self.emit(bind_statement.name + " = ")
        bind_statement.expr.accept(self)

    def visit_CallExpression(self, call_expression):
        self.emit(call_expression.name + "(")
        self.start_list()
        for argument in call_expression.arguments:
            self.start_item()
            argument.accept(self)
            self.end_item()
        self.end_list()
        self.emit(')')

    def emitBlock(self, statements):
        self.emit('{')
        self.inc()
        self.nl()
        for statement in statements:
            statement.accept(self)
            self.nl()
        self.dec()
        self.nl()
        self.emit("}")

    def visit_FunctionStatement(self, function_statement):
        self.emit("function " + function_statement.name + "(")
        self.start_list()
        for param_type, param_name in function_statement.parameters:
            self.start_item()
            if param_type:
                self.emit(param_type + " ")
            self.emit(param_name)
            self.end_item()
        self.end_list()
        self.emit(")")
        self.nl()
        self.emitBlock(function_statement.statements)
        self.nl()
        self.nl()

    def pretty_print(self, node):
        self.start()
        node.accept(self)
        return self.end()

