from .cpAST import get_ast, print_ast

def readast(node, depth, calc):
    calc(node, depth)
    for child in node.get_children():
        print_ast(child, depth + 1, calc)
        
def translate(file_path):
    ast = get_ast(file_path)
    print_ast(ast)
    if file_path.endswith('.c'):
        print("C code AST calculated")
    elif file_path.endswith('.cpp'):
        print("C++ code AST calculated")