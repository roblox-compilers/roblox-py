"""Boolean operation description"""
import ast
_DEFAULT_BOOL_FORMAT = "{left} {operation} {right}"


class BooleanOperationDesc:
    """Binary operation description"""

    OPERATION = {
        ast.And: {
            "value": "and",
            "format": _DEFAULT_BOOL_FORMAT,
        },
        ast.Or: {
            "value": "or",
            "format": _DEFAULT_BOOL_FORMAT,
        },
    }
