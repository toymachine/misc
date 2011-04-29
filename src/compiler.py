import ast
import clj

class Compiler(object):

    def __init__(self):
        self.p_function_stack = []

    def visit_FunctionStatement(self, p_function):

        clj_parameters = [clj.ident(parameter_name) for (_, parameter_name) in p_function.parameters]

        clj_statements = clj.block(1, clj.list([statement.accept(self) for statement in p_function.statements]))

        clj_cfunc = clj.list([clj.DEFN, clj.ident(p_function.name), clj.vector(clj_parameters), clj_statements])

        return clj_cfunc

    def visit_IntegerLiteralExpression(self, p_literalexpr):
        return clj.intliteral(p_literalexpr.value)

    def visit_IdentifierExpression(self, p_identexpr):
        #return jast.VariableExpression(p_identexpr.identifier)
        return clj.ident(p_identexpr.identifier)

    def visit_CallExpression(self, p_callexpr):
        return clj.list([clj.ident(p_callexpr.name)] + [argument.accept(self) for argument in p_callexpr.arguments])

    def visit_BinaryExpression(self, p_binexpr):
        left = p_binexpr.left.accept(self)
        operator = p_binexpr.operator
        right = p_binexpr.right.accept(self)
        return clj.list([clj.ident(operator), left, right])

    def visit_ReturnStatement(self, p_returnstmt):
        return p_returnstmt.expression.accept(self)

    def compile(self, module):

        clj_module = clj.mod([])
        for statement in module.statements:
            assert isinstance(statement, ast.FunctionStatement)
            clj_module.append(statement.accept(self))

        pp = clj.PrettyPrinter()
        print pp.pretty_print(clj_module)
