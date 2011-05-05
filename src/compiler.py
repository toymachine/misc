import ast
import clj



class Compiler(object):


    def __init__(self):
        self.dummy_id = 0

    def dummy_ident(self):
        self.dummy_id += 1
        return clj.ident('__d%d' % self.dummy_id)

    def compile_block(self, statements):
        let_vector = clj.vector([])
        let_list = clj.list([clj.LET, let_vector])

        for statement in statements[:-1]:
            if isinstance(statement, ast.BindStatement):
                let_vector.append(clj.ident(statement.name))
                let_vector.append(statement.expr.accept(self))
            else:
                let_vector.append(self.dummy_ident())
                let_vector.append(statement.accept(self))

        let_list.append(statements[-1].accept(self))

        return let_list

    def visit_FunctionStatement(self, p_function):

        clj_parameters = [clj.ident(parameter_name) for (_, parameter_name) in p_function.parameters]

        clj_cfunc = clj.list([clj.DEFN, clj.ident(p_function.name), clj.vector(clj_parameters), self.compile_block(p_function.statements)])

        return clj_cfunc

    def visit_IntegerLiteralExpression(self, p_literalexpr):
        return clj.intliteral(p_literalexpr.value)

    def visit_ListLiteralExpression(self, p_literalexpr):
        return clj.list([clj.VECTOR] + [expr.accept(self) for expr in p_literalexpr.exprs])

    def visit_StringLiteralExpression(self, p_literalexpr):
        return clj.stringliteral(p_literalexpr.value)

    def visit_IdentifierExpression(self, p_identexpr):
        #return jast.VariableExpression(p_identexpr.identifier)
        return clj.ident(p_identexpr.identifier)

    def visit_IfExpression(self, p_ifexpr):
        #def blockOrExpr(statements):
        #    if len(statements) == 1:
        #        return statements[0].accept(self)
        #    else:
        #        return clj.list([clj.DO] + [stmt.accept(self) for stmt in statements])
        return clj.list([clj.IF, p_ifexpr.expr.accept(self), self.compile_block(p_ifexpr.trueBlock), self.compile_block(p_ifexpr.falseBlock)])

    def visit_CallExpression(self, p_callexpr):
        return clj.list([clj.ident(p_callexpr.name)] + [argument.accept(self) for argument in p_callexpr.arguments])

    #def visit_BindStatement(self, p_bindstmt):
    #    return clj.list([clj.LET, clj.vector([clj.ident(p_bindstmt.name), p_bindstmt.expr.accept(self)])])

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
