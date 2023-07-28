"""Binary operation description"""
import ast


_DEFAULT_FORMAT = "{left} {operation} {right}"

def addfunc(left, right):
    # check if left and right have anything other than 0-9
    # left and right are name objects, so we need to get the id
    if (not isinstance(left.left, ast.Num) or not isinstance(right.right, ast.Num)):
        return "safeadd({left}, {right})"
    else :
        return "{left} + {right}"
class BinaryOperationDesc:
    """Binary operation description"""

    OPERATION = {
        ast.Add: {
            "value": "+",
            "function": addfunc
        },
        ast.Sub: {
            "value": "-",
            "format": _DEFAULT_FORMAT,
        },
        ast.Mult: {
            "value": "*",
            "format": _DEFAULT_FORMAT,
        },
        ast.Div: {
            "value": "/",
            "format": _DEFAULT_FORMAT,
        },
        ast.Mod: {
            "value": "",
            "format": "formatmod({left}, {right})",
        },
        ast.Pow: {
            "value": "",
            "format": "math.pow({left}, {right})",
        },
        ast.FloorDiv: {
            "value": "/",
            "format": "math.floor({left} {operation} {right})",
        },
        ast.LShift: {
            "value": "",
            "format": "bit32.lshift({left}, {right})",
        },
        ast.RShift: {
            "value": "",
            "format": "bit32.rshift({left}, {right})",
        },
        ast.BitOr: {
            "value": "",
            "format": "bit32.bor({left}, {right})",
        },
        ast.BitAnd: {
            "value": "",
            "format": "bit32.band({left}, {right})",
        },
        ast.BitXor: {
            "value": "",
            "format": "bit32.bxor({left}, {right})",
        },
    }
