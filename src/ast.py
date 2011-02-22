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

class BinaryExpr(Expression):
    pass

class PrettyPrinter(object):
    def visitModule(self, module):
        for statement in module.statements:
            statement.__accept__(self)
    
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

    def pretty_print(self, node):
        node.__accept__(self)
        

