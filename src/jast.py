import types
from serializer import Serializer

class Node(object):
    def accept(self, visitor):
        return getattr(visitor, 'visit_' + self.__class__.__name__)(self)

class Module(Node):
    def __init__(self):
        self.package = ''
        self.imports = []
        self.classes = []

class Class(Node):
    def __init__(self, name = ''):
        self.name = name
        self.methods = []
        self.fields = []
        self.modifiers = []
        self.innerClasses = []
        self.extends = []
        self.implements = []

class Method(Node):
    def __init__(self, name = '', type = 'Object', modifiers = None, parameters = None, statements = None):
        self.name = name
        self.type = type
        self.modifiers = modifiers if modifiers is not None else []
        self.parameters = parameters if parameters is not None else []
        self.statements = statements if statements is not None else []

class Parameter(Node):
    def __init__(self, name = '', type = 'Object', isArray = False):
        self.name = name
        self.type = type
        self.isArray = isArray

class Statement(Node):
    def __init__(self):
        pass

class ReturnStatement(Statement):
    def __init__(self, expression = None):
        self.expression = expression

class ThrowStatement(Statement): pass

class EvalExprStatement(Statement):
    def __init__(self, expression):
        Statement.__init__(self)
        self.expression = expression

class IfStatement(Statement):
    pass

class TryCatchStatement(Statement):
    def __init__(self):
        self.statements = []
        self.catches = []

class ForStatement(Statement):
    def __init__(self):
        self.init = None
        self.condition = None
        self.increment = None
        self.statements = []

class ContinueStatement(Statement): pass
class BreakStatement(Statement): pass

class WhileStatement(Statement):
    def __init__(self):
        self.condition = None
        self.statements = []

class DoStatement(Statement):
    def __init__(self):
        self.condition = None
        self.statements = []

class SwitchStatement(Statement):
    def __init__(self):
        self.condition = None
        self.switchCases = []
        self.defaultCase = None

class Expression(Node):
    def __init__(self):
        self.type = 'Object'

class Unknown(Node):
    def __init__(self, msg):
        self.msg = msg

class InstanceOfExpression(Expression):
    pass

class ConditionalExpression(Expression):
    def __init__(self, condition = None, expressionTrue = None, expressionFalse = None):
        Expression.__init__(self)
        self.condition = condition
        self.expressionTrue = expressionTrue
        self.expressionFalse = expressionFalse

class AssignmentExpression(Expression):
    def __init__(self, variable = None, expression = None, type = None):
        Expression.__init__(self)
        self.variable = variable
        self.expression = expression
        self.type = type

class VariableExpression(Expression):
    def __init__(self, name = '', target = ''):
        Expression.__init__(self)
        self.name = name
        self.target = target

class BlockExpression(Expression):
    def __init__(self, statements = None):
        Expression.__init__(self)
        self.statements = statements if statements is not None else []

class BinaryExpression(Expression): pass
class UnaryExpression(Expression): pass

class PostOpExpression(Expression): pass
class PreOpExpression(Expression): pass

class MethodInvocationExpression(Expression):
    def __init__(self, target = None, name = None, parameters = None, static = False):
        Expression.__init__(self)
        self.target = target
        self.name = name
        self.static = False
        if parameters is None:
            self.parameters = []
        else:
            self.parameters = parameters

class NewExpression(Expression):
    def __init__(self, type = 'Object', parameters = None, isArray = False, initializer = None):
        self.type = type
        if parameters is None:
            self.parameters = []
        else:
            self.parameters = parameters
        self.isArray = isArray
        self.initializer = initializer

class InitializerList(Expression):
    def __init__(self, expressions):
        self.expressions = expressions

class CastExpression(Expression):
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

class LiteralInteger(Expression):
    def __init__(self, value):
        self.value = value

class LiteralDouble(Expression):
    def __init__(self, value):
        self.value = value

class LiteralString(Expression):
    def __init__(self, value):
        self.value = value

class LiteralBool(Expression):
    def __init__(self, value):
        self.value = value

class LiteralNull(Expression): pass

BLOCK_STATEMENTS = (IfStatement, WhileStatement, DoStatement, SwitchStatement, ForStatement, TryCatchStatement)

class JavaSerializer(Serializer):
    def __init__(self):
        Serializer.__init__(self)

    def visit_Unknown(self, unknown):
        self.emit('unknown: %s' % unknown.msg)

    def visit_LiteralBool(self, literalBool):
        if literalBool.value:
            self.emit("true")
        else:
            self.emit("false")

    def visit_LiteralInteger(self, literalInteger):
        self.emit(literalInteger.value)

    def visit_LiteralString(self, literalString):
        self.emit('"%s"' % literalString.value)

    def visit_LiteralDouble(self, literalDouble):
        self.emit(repr(literalDouble.value))

    def visit_LiteralNull(self, literalDouble):
        self.emit("null")

    def visit_InitializerList(self, initializerList):
        self.emit("{")
        self.start_list()
        for expression in initializerList.expressions:
            self.start_item()
            expression.accept(self)
            self.end_item()
        self.end_list()
        self.emit("}")

    def visit_MethodInvocationExpression(self, methodInvocationExpression):
        if methodInvocationExpression.target is None:
            pass
        elif isinstance(methodInvocationExpression.target, types.StringTypes):
            self.emit(methodInvocationExpression.target)
            if methodInvocationExpression.static:
                self.emit("::")
            else:
                self.emit(".")
        else:
            methodInvocationExpression.target.accept(self)
            self.emit(".")
        self.emit(methodInvocationExpression.name)
        self.emit("(")
        self.start_list()
        for parameter in methodInvocationExpression.parameters:
            self.start_item()
            parameter.accept(self)
            self.end_item()
        self.end_list()
        self.emit(")")

    def visit_InstanceOfExpression(self, instanceOfExpression):
        instanceOfExpression.expression.accept(self)
        self.emit(" instanceof ")
        self.emit(instanceOfExpression.type)

    def visit_BinaryExpression(self, binaryExpression):
        self.emit("(")
        binaryExpression.left.accept(self)
        self.emit(" ")
        self.emit(binaryExpression.operator)
        self.emit(" ")
        binaryExpression.right.accept(self)
        self.emit(")")

    def visit_UnaryExpression(self, unaryExpression):
        self.emit(unaryExpression.operator)
        self.emit(" ")
        unaryExpression.expression.accept(self)

    def visit_ConditionalExpression(self, conditionalExpression):
        conditionalExpression.condition.accept(self)
        self.emit(" ? ")
        conditionalExpression.expressionTrue.accept(self)
        self.emit(" : ")
        conditionalExpression.expressionFalse.accept(self)

    def visit_PostOpExpression(self, postOpExpression):
        postOpExpression.variable.accept(self)
        self.emit(postOpExpression.operator)

    def visit_PreOpExpression(self, preOpExpression):
        self.emit(preOpExpression.operator)
        preOpExpression.variable.accept(self)

    def visit_AssignmentExpression(self, assignmentExpression):
        if assignmentExpression.type:
            self.emit(assignmentExpression.type)
            self.emit(' ')
        assignmentExpression.variable.accept(self)
        self.emit(' = ')
        assignmentExpression.expression.accept(self)

    def visit_VariableExpression(self, variableExpression):
        if variableExpression.target:
            self.emit(variableExpression.target)
            self.emit('.')
        self.emit(variableExpression.name)

    def visit_EvalExprStatement(self, evalExprStatement):
        evalExprStatement.expression.accept(self)

    def visit_ReturnStatement(self, returnStatement):
        self.emit("return");
        if returnStatement.expression:
            self.emit(" ")
            returnStatement.expression.accept(self)

    def visit_ThrowStatement(self, throwStatement):
        self.emit("throw ");
        throwStatement.expression.accept(self)

    def visit_BlockExpression(self, blockExpression):
        self.emitBlock(blockExpression.statements)

    def visit_NewExpression(self, newExpression):
        self.emit("new " + newExpression.type)
        if newExpression.isArray:
            self.emit("[]")
        else:
            self.emit("(")
            self.start_list()
            for parameter in newExpression.parameters:
                self.start_item()
                parameter.accept(self)
                self.end_item()
            self.end_list()
            self.emit(")")
        if newExpression.initializer:
            self.emit(" ")
            newExpression.initializer.accept(self)

    def visit_CastExpression(self, castExpression):
        self.emit("(")
        self.emit("(")
        self.emit(castExpression.target)
        self.emit(")")
        castExpression.expression.accept(self)
        self.emit(")")

    def visit_IfStatement(self, ifStatement):
        self.emit("if( ")
        ifStatement.expression.accept(self)
        self.emit(" ) ")
        self.nl()
        if ifStatement.statementsTrue:
            self.emitBlock(ifStatement.statementsTrue)
        if ifStatement.statementsFalse:
            self.nl()
            self.emit("else ")
            self.nl()
            self.emitBlock(ifStatement.statementsFalse)

    def visit_SwitchStatement(self, switchStatement):
        self.emit("switch( ")
        switchStatement.condition.accept(self)
        self.emit(" ) ")
        self.nl()
        self.emit("{")
        self.nl()

        for condition, statements in switchStatement.switchCases:
            self.emit("case ")
            condition.accept(self)
            self.emit(": ")
            self.emitBlock(statements)
            self.nl()

        if switchStatement.defaultCase:
            self.emit("default: ")
            self.emitBlock(switchStatement.defaultCase)
            self.nl()

        self.emit("}")

    def visit_TryCatchStatement(self, tryCatchStatement):
        self.emit("try ")
        self.emitBlock(tryCatchStatement.statements)
        for className, variableName, statements in tryCatchStatement.catches:
            self.nl()
            self.emit("catch(")
            self.emit(className)
            self.emit(" ")
            self.emit(variableName)
            self.emit(") ")
            self.emitBlock(statements)

    def visit_ForStatement(self, forStatement):
        self.emit("for(")
        if forStatement.init: forStatement.init.accept(self)
        self.emit("; ")
        if forStatement.condition: forStatement.condition.accept(self)
        self.emit("; ")
        if forStatement.increment: forStatement.increment.accept(self)
        self.emit(") ")
        self.emitBlock(forStatement.statements)

    def visit_WhileStatement(self, whileStatement):
        self.emit("while(")
        whileStatement.condition.accept(self)
        self.emit(") ")
        self.emitBlock(whileStatement.statements)

    def visit_DoStatement(self, doStatement):
        self.emit("do ")
        self.emitBlock(doStatement.statements)
        self.emit(" while (")
        doStatement.condition.accept(self)
        self.emit(")")

    def visit_ContinueStatement(self, continueStatement):
        self.emit("continue")

    def visit_BreakStatement(self, breakStatement):
        self.emit("break")

    def emitBlock(self, statements):
        self.emit("{")
        self.inc()
        for statement in statements:
            self.nl()
            statement.accept(self)
            #only put ; after statement if it is not a block statement
            if not isinstance(statement, BLOCK_STATEMENTS):
                self.emit(";")
        self.dec()
        self.nl()
        self.emit("}")

    def visit_Module(self, module):
        if module.package:
            self.emit("package %s;" % module.package)
            self.nl()
            self.nl()
        for import_ in module.imports:
            self.emit("import %s;" % import_)
            self.nl()
        self.nl()
        for clazz in module.classes:
            clazz.accept(self)

    def emitModifiers(self, modifiers):
        if modifiers:
            self.emit(' '.join(modifiers) + ' ')


    def visit_Method(self, method):
        self.emitModifiers(method.modifiers)
        self.emit(method.type + " " + method.name + "(")
        self.start_list()
        for param in method.parameters:
            self.start_item()
            self.emit(param.type)
            self.emit(" ")
            self.emit(param.name)
            if param.isArray:
                self.emit("[]")
            self.end_item()
        self.end_list()
        self.emit(")")
        self.nl()
        self.emitBlock(method.statements)

    def visit_Class(self, clazz):
        self.nl()
        self.emitModifiers(clazz.modifiers)
        self.emit("class " + clazz.name)
        if clazz.extends:
            self.emit(" extends " + ', '.join(clazz.extends))
        if clazz.implements:
            self.emit(" implements " + ", ".join(clazz.implements))
        self.nl()
        self.emit("{")
        self.inc()

        for field, modifiers, type, init in clazz.fields:
            self.nl()
            self.emit(' '.join(modifiers) + " " + type + " ")
            self.emit(field)
            if init:
                self.emit(" = ")
                init.accept(self)
            self.emit(';')
            self.dec()
        if clazz.fields:
            self.nl()

        for innerClass in clazz.innerClasses:
            self.nl()
            innerClass.accept(self)

        for method in clazz.methods:
            self.nl()
            method.accept(self)

        self.dec()
        self.nl()
        self.emit("}")

    def serialize(self, module):
        try:
            self.start()
            module.accept(self)
            return self.end()
        except:
            print self.buffers
            raise

