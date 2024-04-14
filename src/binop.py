"""Binary operation description"""
import ast
_DEFAULT_BIN_FORMAT = "{left} {operation} {right}"


class BinaryOperationDesc:
    """Binary operation description"""

    OPERATION = {
        ast.Add: {
            "value": "+",
            "format": "(safeadd({left}, {right}))",
            "depend": "safeadd",
        },
        ast.Sub: {
            "value": "-",
            "format": _DEFAULT_BIN_FORMAT,            
	    "depend": "",
        },
        ast.Mult: {
            "value": "*",
            "format": _DEFAULT_BIN_FORMAT,
	    "depend": "",
        },
        ast.Div: {
            "value": "/",
            "format": _DEFAULT_BIN_FORMAT,
            "depend": "",
        },
        ast.Mod: {
            "value": "%",
            "format": _DEFAULT_BIN_FORMAT,
	    "depend": "",
        },
        ast.Pow: {
            "value": "^",
            "format": _DEFAULT_BIN_FORMAT,
	    "depend": "",
        },
        ast.FloorDiv: {
            "value": "/",
            "format": "math.floor({left} {operation} {right})",
	    "depend": "",
        },
        ast.LShift: {
            "value": "",
            "format": "bit32.lshift({left}, {right})",
	    "depend": "",
        },
        ast.RShift: {
            "value": "",
            "format": "bit32.rshift({left}, {right})",
	    "depend": "",
        },
        ast.BitOr: {
            "value": "",
            "format": "bit32.bor({left}, {right})",
	    "depend": "",
        },
        ast.BitAnd: {
            "value": "",
            "format": "bit32.band({left}, {right})",
	    "depend": "",
        },
        ast.BitXor: {
            "value": "",
            "format": "bit32.bxor({left}, {right})",
	    "depend": "",
        },
    }
