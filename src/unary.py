"""Unary operation description"""

import ast

_DEFAULT_UN_FORMAT = "{operation}{value}"


class UnaryOperationDesc:
    """Unary operation description"""

    OPERATION = {
        ast.USub: {
            "value": "-",
            "format": _DEFAULT_UN_FORMAT,
        },
        ast.UAdd: {
            "value": "",
            "format": _DEFAULT_UN_FORMAT,
        },
        ast.Not: {
            "value": "not",
            "format": "not {value}",
        },
        ast.Invert: {
            "value": "~",
            "format": "bit32.bnot({value})",
        },
    }
