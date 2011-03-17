import types
from serializer import Serializer

class ASTObject(object):
    def __visit__(self, visitor):
        acceptorName = 'accept' + self.__class__.__name__
        getattr(visitor, acceptorName)(self)

class Module(ASTObject):
    def __init__(self):
        self.package = ''
        self.imports = []
        self.classes = []

class Class(ASTObject):
    def __init__(self, name = ''):
        self.name = name
        self.methods = []
        self.fields = []
        self.modifiers = []
        self.innerClasses = []
        self.extends = []
        self.implements = []

class Method(ASTObject):
    def __init__(self, name = '', type = 'Object', modifiers = [], parameters = [], statements = []):
        self.name = name
        self.type = type
        self.modifiers = modifiers
        self.parameters = parameters
        self.statements = statements

class Parameter(ASTObject):
    def __init__(self, name = '', type = 'Object', isArray = False):
        self.name = name
        self.type = type
        self.isArray = isArray

class Statement(ASTObject):
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

class Expression(ASTObject):
    def __init__(self):
        self.type = 'Object'

class Unknown(ASTObject):
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
    def __init__(self, statements = []):
        Expression.__init__(self)
        self.statements = statements

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

    def acceptUnknown(self, unknown):
        self.emit('unknown: %s' % unknown.msg)

    def acceptLiteralBool(self, literalBool):
        if literalBool.value:
            self.emit("true")
        else:
            self.emit("false")

    def acceptLiteralInteger(self, literalInteger):
        self.emit(literalInteger.value)

    def acceptLiteralString(self, literalString):
        self.emit('"%s"' % literalString.value)

    def acceptLiteralDouble(self, literalDouble):
        self.emit(repr(literalDouble.value))

    def acceptLiteralNull(self, literalDouble):
        self.emit("null")

    def acceptInitializerList(self, initializerList):
        self.emit("{")
        self.start_list()
        for expression in initializerList.expressions:
            self.startItem()
            expression.__visit__(self)
            self.endItem()
        self.end_list()
        self.emit("}")

    def acceptMethodInvocationExpression(self, methodInvocationExpression):
        if methodInvocationExpression.target is None:
            pass
        elif isinstance(methodInvocationExpression.target, types.StringTypes):
            self.emit(methodInvocationExpression.target)
            if methodInvocationExpression.static:
                self.emit("::")
            else:
                self.emit(".")
        else:
            methodInvocationExpression.target.__visit__(self)
            self.emit(".")
        self.emit(methodInvocationExpression.name)
        self.emit("(")
        self.start_list()
        for parameter in methodInvocationExpression.parameters:
            self.startItem()
            parameter.__visit__(self)
            self.endItem()
        self.end_list()
        self.emit(")")

    def acceptInstanceOfExpression(self, instanceOfExpression):
        instanceOfExpression.expression.__visit__(self)
        self.emit(" instanceof ")
        self.emit(instanceOfExpression.type)

    def acceptBinaryExpression(self, binaryExpression):
        binaryExpression.left.__visit__(self)
        self.emit(" ")
        self.emit(binaryExpression.op)
        self.emit(" ")
        binaryExpression.right.__visit__(self)

    def acceptUnaryExpression(self, unaryExpression):
        self.emit(unaryExpression.op)
        self.emit(" ")
        unaryExpression.expression.__visit__(self)

    def acceptConditionalExpression(self, conditionalExpression):
        conditionalExpression.condition.__visit__(self)
        self.emit(" ? ")
        conditionalExpression.expressionTrue.__visit__(self)
        self.emit(" : ")
        conditionalExpression.expressionFalse.__visit__(self)

    def acceptPostOpExpression(self, postOpExpression):
        postOpExpression.variable.__visit__(self)
        self.emit(postOpExpression.op)

    def acceptPreOpExpression(self, preOpExpression):
        self.emit(preOpExpression.op)
        preOpExpression.variable.__visit__(self)

    def acceptAssignmentExpression(self, assignmentExpression):
        if assignmentExpression.type:
            self.emit(assignmentExpression.type)
            self.emit(' ')
        assignmentExpression.variable.__visit__(self)
        self.emit(' = ')
        assignmentExpression.expression.__visit__(self)

    def acceptVariableExpression(self, variableExpression):
        if variableExpression.target:
            self.emit(variableExpression.target)
            self.emit('.')
        self.emit(variableExpression.name)

    def acceptEvalExprStatement(self, evalExprStatement):
        evalExprStatement.expression.__visit__(self)

    def acceptReturnStatement(self, returnStatement):
        self.emit("return");
        if returnStatement.expression:
            self.emit(" ")
            returnStatement.expression.__visit__(self)

    def acceptThrowStatement(self, throwStatement):
        self.emit("throw ");
        throwStatement.expression.__visit__(self)

    def acceptBlockExpression(self, blockExpression):
        self.emitBlock(blockExpression.statements)

    def acceptNewExpression(self, newExpression):
        self.emit("new " + newExpression.type)
        if newExpression.isArray:
            self.emit("[]")
        else:
            self.emit("(")
            self.start_list()
            for parameter in newExpression.parameters:
                self.startItem()
                parameter.__visit__(self)
                self.endItem()
            self.end_list()
            self.emit(")")
        if newExpression.initializer:
            self.emit(" ")
            newExpression.initializer.__visit__(self)

    def acceptCastExpression(self, castExpression):
        self.emit("(")
        self.emit("(")
        self.emit(castExpression.target)
        self.emit(")")
        castExpression.expression.__visit__(self)
        self.emit(")")

    def acceptIfStatement(self, ifStatement):
        self.emit("if( ")
        ifStatement.expression.__visit__(self)
        self.emit(" ) ")
        self.nl()
        if ifStatement.statementsTrue:
            self.emitBlock(ifStatement.statementsTrue)
        if ifStatement.statementsFalse:
            self.nl()
            self.emit("else ")
            self.nl()
            self.emitBlock(ifStatement.statementsFalse)

    def acceptSwitchStatement(self, switchStatement):
        self.emit("switch( ")
        switchStatement.condition.__visit__(self)
        self.emit(" ) ")
        self.nl()
        self.emit("{")
        self.nl()

        for condition, statements in switchStatement.switchCases:
            self.emit("case ")
            condition.__visit__(self)
            self.emit(": ")
            self.emitBlock(statements)
            self.nl()

        if switchStatement.defaultCase:
            self.emit("default: ")
            self.emitBlock(switchStatement.defaultCase)
            self.nl()

        self.emit("}")

    def acceptTryCatchStatement(self, tryCatchStatement):
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

    def acceptForStatement(self, forStatement):
        self.emit("for(")
        if forStatement.init: forStatement.init.__visit__(self)
        self.emit("; ")
        if forStatement.condition: forStatement.condition.__visit__(self)
        self.emit("; ")
        if forStatement.increment: forStatement.increment.__visit__(self)
        self.emit(") ")
        self.emitBlock(forStatement.statements)

    def acceptWhileStatement(self, whileStatement):
        self.emit("while(")
        whileStatement.condition.__visit__(self)
        self.emit(") ")
        self.emitBlock(whileStatement.statements)

    def acceptDoStatement(self, doStatement):
        self.emit("do ")
        self.emitBlock(doStatement.statements)
        self.emit(" while (")
        doStatement.condition.__visit__(self)
        self.emit(")")

    def acceptContinueStatement(self, continueStatement):
        self.emit("continue")

    def acceptBreakStatement(self, breakStatement):
        self.emit("break")

    def emitBlock(self, statements):
        self.emit("{")
        for statement in statements:
            self.nl()
            statement.__visit__(self)
            #only put ; after statement if it is not a block statement
            if not isinstance(statement, BLOCK_STATEMENTS):
                self.emit(";")
            self.dec()
        self.nl()
        self.emit("}")

    def acceptModule(self, module):
        self.emit("package %s;" % module.package)
        self.nl()
        self.nl()
        for import_ in module.imports:
            self.emit("import %s;" % import_)
            self.nl()
        self.nl()
        for clazz in module.classes:
            clazz.__visit__(self)

    def emitModifiers(self, modifiers):
        if modifiers:
            self.emit(' '.join(modifiers) + ' ')


    def acceptMethod(self, method):
        self.emitModifiers(method.modifiers)
        self.emit(method.type + " " + method.name + "(")
        self.start_list()
        for param in method.parameters:
            self.startItem()
            self.emit(param.type)
            self.emit(" ")
            self.emit(param.name)
            if param.isArray:
                self.emit("[]")
            self.endItem()
        self.end_list()
        self.emit(")")
        self.nl()
        self.emitBlock(method.statements)

    def acceptClass(self, clazz):
        self.nl()
        self.emitModifiers(clazz.modifiers)
        self.emit("class " + clazz.name)
        if clazz.extends:
            self.emit(" extends " + ', '.join(clazz.extends))
        if clazz.implements:
            self.emit(" implements " + ", ".join(clazz.implements))
        self.nl()
        self.emit("{")

        for field, modifiers, type, init in clazz.fields:
            self.nl()
            self.emit(' '.join(modifiers) + " " + type + " ")
            self.emit(field)
            if init:
                self.emit(" = ")
                init.__visit__(self)
            self.emit(';')
            self.dec()
        if clazz.fields:
            self.nl()

        for innerClass in clazz.innerClasses:
            self.nl()
            innerClass.__visit__(self)
            self.nl()
            self.dec()

        for method in clazz.methods:
            self.nl()
            method.__visit__(self)
            self.nl()
            self.dec()
        self.nl()
        self.emit("}")

    def serialize(self, module):
        try:
            self.start()
            module.__visit__(self)
            return self.end()
        except:
            print self.buffers
            raise

