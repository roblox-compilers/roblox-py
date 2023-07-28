"""Python to lua translator class"""
import ast
import os
import sys
if not (os.path.dirname(os.path.abspath(__file__)).startswith(sys.path[-1])):
    from config import Config
    from nodevisitor import NodeVisitor
    from header import header, pyfooter
    from luainit import initcode, allfunctions, generatewithlibraries, robloxfunctions
else:
    from .config import Config
    from .nodevisitor import NodeVisitor

    from .header import header, pyfooter
    from .luainit import initcode, allfunctions, generatewithlibraries, robloxfunctions

class Translator:
    """Python to lua main class translator"""
    def __init__(self, config=None, show_ast=False):
        self.config = config if config is not None else Config()
        self.show_ast = show_ast

        self.output = []

    def translate(self, pycode):
        """Translate python code to lua code"""
        py_ast_tree = ast.parse(pycode)

        visitor = NodeVisitor(config=self.config)

        if self.show_ast: # 
            print(ast.dump(py_ast_tree))

        visitor.visit(py_ast_tree)

        self.output = visitor.output
        # check every single line for function calls
        functions = []
        for i in range(len(self.to_code().split("\n"))):
            # check if a function is being called, like print()
            
            for function in (allfunctions+robloxfunctions):
                if function in self.to_code().split("\n")[i] and function not in functions:
                    functions.append(function)
                    
                    
        # create header for function calls
        newheader = header(functions)
    
        return newheader+self.to_code()+pyfooter

    def to_code(self, code=None, indent=0):
        """Create a lua code from the compiler output"""
        code = code if code is not None else self.output

        def add_indentation(line):
            """Add indentation to the given line"""
            indentation_width = 4
            indentation_space = " "

            indent_copy = max(indent, 0)

            return indentation_space * indentation_width * indent_copy + line

        lines = []
        for line in code:
            if isinstance(line, str):
                lines.append(add_indentation(line))
            elif isinstance(line, list):
                sub_code = self.to_code(line, indent + 1)
                lines.append(sub_code)

        return "\n".join(lines)

    @staticmethod
    def get_luainit(items):
        return generatewithlibraries(items)
