import ast
import jast


class Compiler(object):

    def __init__(self):
        self.p_function_stack = []

    def visit_FunctionStatement(self, p_function):

        self.p_function_stack.append(p_function)

        #print self.p_function_stack

        j_funclass = jast.Class(p_function.name)
        j_funclass.modifiers.append("public")
        j_funclass.modifiers.append("static")
        j_funclass.implements.append("Function")

        #constructor (for closure)
        j_constructor = jast.Method(p_function.name, type = None, modifiers = ['public'])

        #call method
        j_callmethod = jast.Method('call', type = 'int', modifiers = ['public'])
        for parameter_type, parameter_name in p_function.parameters:
            j_callmethod.parameters.append(jast.Parameter(parameter_name, parameter_type))

        for statement in p_function.statements:
            j_callmethod.statements.append(statement.accept(self))

        j_funclass.methods.append(j_constructor)
        j_funclass.methods.append(j_callmethod)

        self.j_funclasses.append(j_funclass)

        #create the closure and catch the environment
        j_assignment = jast.AssignmentExpression(jast.VariableExpression('v_' + p_function.name), jast.NewExpression(p_function.name), p_function.name)

        self.p_function_stack.pop()

        return j_assignment

    def visit_IntegerLiteralExpression(self, p_literalexpr):
        return jast.LiteralInteger(p_literalexpr.value)

    def visit_IdentifierExpression(self, p_identexpr):
        return jast.VariableExpression(p_identexpr.identifier)

    def visit_BinaryExpression(self, p_binexpr):
        j_binexpr = jast.BinaryExpression()
        j_binexpr.left = p_binexpr.left.accept(self)
        j_binexpr.operator = p_binexpr.operator
        j_binexpr.right = p_binexpr.right.accept(self)
        return j_binexpr

    def visit_ReturnStatement(self, p_returnstmt):
        j_returnstmt = jast.ReturnStatement()
        j_returnstmt.expression = p_returnstmt.expression.accept(self)
        return j_returnstmt

    def compile(self, module):


        #print module

        pp = ast.PrettyPrinter()
        #print pp.pretty_print(module)

        j_module = jast.Module()
        self.j_funclasses = []

        for statement in module.statements:
            assert isinstance(statement, ast.FunctionStatement)
            statement.accept(self)

        j_moduleclass = jast.Class("Test")
        j_moduleclass.modifiers.append("public")
        j_module.classes.append(j_moduleclass)

        for j_funclass in self.j_funclasses:
            j_moduleclass.innerClasses.append(j_funclass)

        jserializer = jast.JavaSerializer()
        print jserializer.serialize(j_module)

