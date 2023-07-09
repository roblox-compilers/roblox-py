import clang.cindex

class NodeVisitor:
    def __init__(self):
        self.lua_code = ""

    def visit_translation_unit(self, node):
        # Visit child nodes of the translation unit
        for child in node.get_children():
            self.visit_node(child)

    def visit_function_decl(self, node):
        # Process function declarations
        function_name = node.spelling
        self.lua_code += f"function {function_name}()\n"
        self.visit_compound_stmt(node.get_children())  # Visit the body of the function
        self.lua_code += "end\n\n"

    def visit_var_decl(self, node):
        # Process variable declarations
        variable_name = node.spelling
        self.lua_code += f"local {variable_name}\n"

    def visit_compound_stmt(self, node):
        # Process compound statements (e.g., function bodies, loops, etc.)
        self.lua_code += "{\n"
        for child in node:
            self.visit_node(child)
        self.lua_code += "}\n"

    def visit_call_expr(self, node):
        # Process function calls
        function_name = node.spelling
        self.lua_code += f"{function_name}()\n"

    def visit_decl_ref_expr(self, node):
        # Process variable references
        variable_name = node.spelling
        self.lua_code += f"{variable_name}"

    def visit_node(self, node):
        # Dispatch visitation based on node kind
        if node.kind == clang.cindex.CursorKind.TRANSLATION_UNIT:
            self.visit_translation_unit(node)
        elif node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            self.visit_function_decl(node)
        elif node.kind == clang.cindex.CursorKind.VAR_DECL:
            self.visit_var_decl(node)
        elif node.kind == clang.cindex.CursorKind.COMPOUND_STMT:
            self.visit_compound_stmt(node)
        elif node.kind == clang.cindex.CursorKind.CALL_EXPR:
            self.visit_call_expr(node)
        elif node.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
            self.visit_decl_ref_expr(node)

        # Recursively visit child nodes
        for child in node.get_children():
            self.visit_node(child)

    def get_lua_code(self):
        return self.lua_code