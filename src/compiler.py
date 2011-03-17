import ast
import jast


class Compiler(object):
    def compile(self, module):


        print module

        pp = ast.PrettyPrinter()
        print pp.pretty_print(module)

        jmodule = jast.Module()
        jmoduleclass = jast.Class("Test")
        jmoduleclass.modifiers.append("public")
        for statement in module.statements:
            assert isinstance(statement, ast.FunctionStmt)
            jfuncclass = jast.Class(statement.name)
            jfuncclass.modifiers.append("public")
            jfuncclass.modifiers.append("static")
            jfuncclass.implements.append("Function")

            #call method
            jcallmethod = jast.Method('call', type = 'int', modifiers = ['public'])
            jfuncclass.methods.append(jcallmethod)
            jmoduleclass.innerClasses.append(jfuncclass)


        jmodule.classes.append(jmoduleclass)
        jserializer = jast.JavaSerializer()
        print jserializer.serialize(jmodule)

