"""Python to lua translator class"""
import ast
import sys
from config import Config
from nodevisitor import NodeVisitor
from log import error
from const import HEADER
from libs import *
import libs

DEPEND = libs.DEPENDENCY
class Translator:
    """Python to lua main class translator"""
    def __init__(self, config=None, show_ast=False):
        self.config = config if config is not None else Config()
        self.show_ast = show_ast

        self.output = []

    def translate(self, pycode, fn, isAPI = False, export = True, reqfile = False, useRequire = False, pyRight = False):
        """Translate python code to lua code"""
        global DEPEND
        if not reqfile:
            if isAPI: 
                py_ast_tree = ast.parse(pycode)
            else:
                try:
                    # code that uses ast
                    py_ast_tree = ast.parse(pycode)
                except SyntaxError as err:
                    sys.stderr.write("\033[1;31m" + "syntax error: " + "\033[0m" + str(err) + "\n")
                    sys.exit(1)
                
            visitor = NodeVisitor(config=self.config)

            if self.show_ast:
                print(ast.dump(py_ast_tree))

            visitor.visit(py_ast_tree)
            
            self.output = visitor.output
            
            # Remove duplicates from dependencies (list)
            dependencies = list(set(visitor.get_dependencies()))
            
            exports = list(set(visitor.get_exports()))
            
            if fn:
                dependencies.append("fn")
            if export and exports != []:
                FOOTER = "\n\n--> exports\n"
                FOOTER += "if not script:IsA(\"BaseScript\") then\n\treturn {\n"
                for export in exports:
                    FOOTER += f"\t\t[\"{export}\"] = {export},\n"
                FOOTER += "\t}\nend"
            else:
                FOOTER = ""
            
        if reqfile:
            dependencies = ["class", "dict", "list", "in", "fn", "safeadd", "is"]
        if not useRequire:
            for depend in dependencies:
                # set
                
                if depend == "list":
                    DEPEND += LIST
                elif depend == "dict":
                    DEPEND += DICT
                elif depend == "class":
                    DEPEND += CLASS    
                elif depend == "in":
                    DEPEND += IN
                elif depend == "fn":
                    DEPEND += FN
                elif depend == "safeadd":
                    DEPEND += ADD
                elif depend == "is":
                    DEPEND += IS
                else:
                    error("Auto-generated dependency unhandled '{}', please report this issue on Discord or Github".format(depend))
    
        if not reqfile:           
            DEPEND += "\n\n--> code begin\n"  
        else:
            allDepends = ""
            for depend in libs.libs:
                allDepends += f"[\"{depend}\"] = {depend},"
            DEPEND += "\n\nreturn {"+allDepends+"}\n"
            return DEPEND
        
        CODE = self.to_code()
        ERRS = "\n\n--> error handling\n"
        
        for i in errs:
            if ("error("+i+"(") in CODE:
                ERRS += f"""function {i}(errorMessage)
    return ("[roblox-py] {i}: " .. errorMessage)
end
"""
            
        for i in libs.libs:
            if i in CODE:
                DEPEND += f"{i} = py.{i}\n"
                
        DEPEND += "\n\n--> code start\n"
            

        return HEADER + TYPS + ERRS + DEPEND + CODE + FOOTER

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
    def get_luainit(): # Return STDlib
        return """"""
