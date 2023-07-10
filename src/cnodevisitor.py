import clang.cindex
from . import colortext

# TODO:
## Add depth/indentation to the code
## Add all possible node types

class NodeVisitor:
    def __init__(self):
        self.lua_code = ""

    def TRANSLATION_UNIT(self, node, depth=0):
        # Visit child nodes of the translation unit
        for child in node.get_children():
            self.visit_node(child)

    def FUNCTION_DECL(self, node, depth=0):
        # Process function declarations
        function_name = node.spelling
        self.lua_code += f"function {function_name}()\n"
        self.visit_compound_stmt(node.get_children())

    def VAR_DECL(self, node, depth=0):
        # Process variable declarations
        variable_name = node.spelling
        self.lua_code += f"local {variable_name}\n"

    def COMPOUND_STMT(self, node, depth=0):
        # Process compound statements (e.g., function bodies, loops, etc.)
        self.lua_code += "\n"
        if type(node) == list:
            for child in node:
                self.visit_node(child)
        else:
            for child in node.get_children():
                self.visit_node(child)
        self.lua_code += "end\n"

    def CALL_EXPR(self, node, depth=0):
        # Process function calls
        function_name = node.spelling
        self.lua_code += f"{function_name}()\n"

    def DECL_REF_EXPR(self, node, depth=0):
        # Process variable references
        variable_name = node.spelling
        self.lua_code += f"{variable_name}"

    
    def visit_node(self, node, depth=0):
        # Dispatch visitation based on node kind
        if self[node.kind] is not None:
            self[node.kind](node, depth+1)
        else:
            print(colortext.yellow(f"Warning: No visitor method for {node.kind}"))

        # Recursively visit child nodes
        for child in node.get_children():
            self.visit_node(child)

    def get_lua_code(self):
        return self.lua_code