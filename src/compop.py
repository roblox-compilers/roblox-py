"""Compare operation description"""
import ast

class CompareOperationDesc:
    """Compare operation description"""

    OPERATION = {
        ast.Eq: "==",
        ast.NotEq: "~=",
        ast.Lt: "<",
        ast.LtE: "<=",
        ast.Gt: ">",
        ast.GtE: ">=",
        ast.In: {
            "format": "op_in({left}, {right})",
            "depend": "in",
        },
        ast.NotIn: {
            "format": "not op_in({left}, {right})",
            "depend": "in",
        },
        ast.Is: {
            "format": "op_is({left}, {right})",
            "depend": "is",
        },
        ast.IsNot: {
            "format": "not op_is({left}, {right})",
            "depend": "is",
        },
    }
    
