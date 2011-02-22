class Node(object):
    def __accept__(self, visitor):
        getattr(visitor, 'visit' + self.__class__.__name__)(self)

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

class PrettyPrinter(object):
    def visitModule(self, module):
        for statement in module.statements:
            statement.__accept__(self)

    def visitIntegerLiteralExpression(self, integer_literal_expression):
        print integer_literal_expression.value

    def visitIdentifierExpression(self, identifier_expression):
        print identifier_expression.identifier

    def visitBinaryExpression(self, binary_expression):
        print "("
        binary_expression.left.__accept__(self)
        print binary_expression.operator
        binary_expression.right.__accept__(self) 
        print ")"

    def visitReturnStmt(self, return_statement):
        print "return "
        return_statement.expression.__accept__(self)

    def visitFunctionStmt(self, function_statement):
        print "function " + function_statement.name + "("
        for arg_type, arg_name in function_statement.arguments:
            print arg_type, arg_name, ",",
        print ") {"
        for statement in function_statement.statements:
            statement.__accept__(self)
        print "}"

    def pretty_print(self, node):
        node.__accept__(self)
        

