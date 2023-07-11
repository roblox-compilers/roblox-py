# THIS IS OLD DO NOT USE


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
        
        for child in node.get_children():
            self.visit_node(child)

    def COMPOUND_STMT(self, node, depth=0):
        if type(node) == list:
            all = node
        else:
            all = node.get_children()  
            
        for child in all:
            self.visit_node(child, depth+1)
            
        self.lua_code += "end\n"
        
        for child in node.get_children():
            self.visit_node(child)
    
    def DECL_STMT(self, node, depth=0):
        self.visit_node(node.get_children(), depth+1)
        
        for child in node.get_children():
            self.visit_node(child)
        
    def BINARY_OPERATOR(self, node, depth=0):
        # Process binary operators
        operator = node.spelling
        self.lua_code += f"{operator} "
        
        for child in node.get_children():
            self.visit_node(child)
        
    def UNARY_OPERATOR(self, node, depth=0):
        # Process unary operators
        operator = node.spelling
        self.lua_code += f"{operator} "
        
        for child in node.get_children():
            self.visit_node(child)
        
    def DECL_REF_EXPR(self, node, depth=0):
        # Process variable references
        variable_name = node.spelling
        self.lua_code += f"{variable_name} "
        
        for child in node.get_children():
            self.visit_node(child)
        
    def INTEGER_LITERAL(self, node, depth=0):
        # Process integer literals
        value = node.spelling
        self.lua_code += f"{value} "
        
        for child in node.get_children():
            self.visit_node(child)
        
    def FLOATING_LITERAL(self, node, depth=0):
        # Process floating point literals
        value = node.spelling
        self.lua_code += f"{value} "
        
        for child in node.get_children():
            self.visit_node(child)
        
    def STRING_LITERAL(self, node, depth=0):
        # Process string literals
        value = node.spelling
        self.lua_code += f"{value} "
        
        for child in node.get_children():
            self.visit_node(child)
        
    def CHARACTER_LITERAL(self, node, depth=0):
        # Process character literals
        value = node.spelling
        self.lua_code += f"{value} "
        
        for child in node.get_children():
            self.visit_node(child)
        
    

    
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