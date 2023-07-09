"""
Dedicated to parsing C/C++ code into ASTs using libclang.
Pass the code on to the C(++) translator.
"""

import clang.cindex as clang

def get_ast(file_path):
    index = clang.Index.create()
    translation_unit = index.parse(file_path)
    return translation_unit.cursor

def print_ast(node, depth=0):
    print('  ' * depth + str(node.kind) + ' : ' + node.spelling)
    for child in node.get_children():
        print_ast(child, depth + 1)

# C code example
c_file = 'test.c'
c_ast = get_ast(c_file)
print('C AST:')
print_ast(c_ast)

# C++ code example
cpp_file = 'test.cpp'
cpp_ast = get_ast(cpp_file)
print('C++ AST:')
print_ast(cpp_ast)
