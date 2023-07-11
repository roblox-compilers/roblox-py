# THIS IS OLD DO NOT USE

from .cpAST import get_ast, print_ast
from .cnodevisitor import NodeVisitor

def readast(node, depth, calc):
    calc(node, depth)
    for child in node.get_children():
        print_ast(child, depth + 1, calc)
        
def translate(file_path):
    ast = get_ast(file_path)
    print_ast(ast)

    newNodeVisitor = NodeVisitor()
    newNodeVisitor.visit_node(ast)
    
    print(newNodeVisitor.get_lua_code())