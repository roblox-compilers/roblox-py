#!/usr/bin/env python3
import sys, ast, yaml, re, os, astunparse
from pprint import pprint
from pathlib import Path

#### CONSTANTS ####
VERSION = "3.0.0"
TAB = "\t\b\b\b\b"

#### COMPILER ####
"""Config"""
class Config:
    """Translator config."""
    def __init__(self, filename=None):
        self.data = {
            "class": {
                "return_at_the_end": False,
            },
        }

        if filename is not None:
            self.load(filename)

    def load(self, filename):
        """Load config from the file"""
        try:
            with open(filename, "r") as stream:
                data = yaml.load(stream)
                self.data.update(data)
        except FileNotFoundError:
            pass # Use a default config if the file not found
        except yaml.YAMLError as ex:
            print(ex)

    def __getitem__(self, key):
        """Get data values"""
        return self.data[key]

"""Binary operation description"""
_DEFAULT_BIN_FORMAT = "{left} {operation} {right}"


class BinaryOperationDesc:
    """Binary operation description"""

    OPERATION = {
        ast.Add: {
            "value": "+",
            "format": _DEFAULT_BIN_FORMAT,
        },
        ast.Sub: {
            "value": "-",
            "format": _DEFAULT_BIN_FORMAT,
        },
        ast.Mult: {
            "value": "*",
            "format": _DEFAULT_BIN_FORMAT,
        },
        ast.Div: {
            "value": "/",
            "format": _DEFAULT_BIN_FORMAT,
        },
        ast.Mod: {
            "value": "%",
            "format": _DEFAULT_BIN_FORMAT,
        },
        ast.Pow: {
            "value": "^",
            "format": _DEFAULT_BIN_FORMAT,
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
"""Boolean operation description"""
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

"""Compare operation description"""

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
            "format": "operator_in({left}, {right})",
        },
        ast.NotIn: {
            "format": "not operator_in({left}, {right})",
        },
    }
    
"""Name constant description"""


class NameConstantDesc:
    """Name constant description"""

    NAME = {
        None: "nil",
        True: "true",
        False: "false",
    }
    
"""Unary operation description"""

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
"""Token end mode"""
from enum import Enum


class TokenEndMode(Enum):
    """This enum represents token end mode"""
    LINE_FEED = 0
    LINE_CONTINUE = 1
    
"""Class for the symbols stack"""
class SymbolsStack:
    """Class for the symbols stack"""
    def __init__(self):
        self.symbols = [[]]

    def add_symbol(self, name):
        """Add a new symbol to the curent stack"""
        self.symbols[-1].append(name)

    def exists(self, name):
        """Check symbol is exists in the current stack"""
        for stack in self.symbols:
            if name in stack:
                return True
        return False

    def push(self):
        """Push the symbols stack"""
        self.symbols.append([])

    def pop(self):
        """Pop the symbols stack"""
        self.symbols.pop()

"""Class to store the python code context"""
class Context:
    """Class to store the python code context"""
    def __init__(self, values=None):
        values = values if values is not None else {
            "token_end_mode": TokenEndMode.LINE_FEED,
            "class_name": "",
            "locals": SymbolsStack(),
            "globals": SymbolsStack(),  # Not working yet
            "loop_label_name": "",
            "docstring": False,
        }

        self.ctx_stack = [values]

    def last(self):
        """Return actual context state"""
        return self.ctx_stack[-1]

    def push(self, values):
        """Push new context state with new values"""
        value = self.ctx_stack[-1].copy()
        value.update(values)
        self.ctx_stack.append(value)

    def pop(self):
        """Pop last context state"""
        assert len(self.ctx_stack) > 1, "Pop context failed. This is a last context in the stack."
        return self.ctx_stack.pop()

"""Label counter for the loops continue"""
class LoopCounter:
    """Loop counter"""
    COUNTER = 0

    @staticmethod
    def get_next():
        """Return next loop continue label name"""
        LoopCounter.COUNTER += 1
        return "loop_label_{}".format(LoopCounter.COUNTER)

"""Node visitor"""
dependencies = []

class NodeVisitor(ast.NodeVisitor):
    LUACODE = "luau"

    """Node visitor"""
    def __init__(self, context=None, config=None):
        self.context = context if context is not None else Context()
        self.config = config
        self.last_end_mode = TokenEndMode.LINE_FEED
        self.output = []

    def visit_Assign(self, node):
        """Visit assign"""
        target = self.visit_all(node.targets[0], inline=True)
        value = self.visit_all(node.value, inline=True)

        local_keyword = ""

        last_ctx = self.context.last()

        if last_ctx["class_name"]:
            target = ".".join([last_ctx["class_name"], target])

        if "." not in target and not last_ctx["locals"].exists(target):
            local_keyword = "local "
            last_ctx["locals"].add_symbol(target)


        self.emit("{local}{target} = {value}".format(local=local_keyword,
                                                     target=target,
                                                     value=value))

        ### MATCHES ###
    def visit_Match(self, node):
        """Visit match"""
        for case in node.cases:
            if hasattr(case.pattern, "value"):
                first = ""
                if case is node.cases[0]:
                    first = ""
                else:
                    first = "else"
                    
                self.emit("{}if {} == {} then".format(first, self.visit_all(node.subject, inline=True), case.pattern.value.s))
                self.visit_all(case.body)
            else:
                self.emit("else")
                self.visit_all(case.body)
        self.emit("end")
        
    def visit_MatchValue(self, node):
        """Visit match value"""
        return self.visit_all(node.value, inline=True)
    def visit_MatchCase(self, node):
        """Visit match case"""
        return self.visit_all(node.body)
    
    def visit_MatchPattern(self, node):
        """Visit match pattern"""
        return self.visit_all(node.pattern, inline=True)
    
    def visit_MatchSingleton(self, node):
        """Visit match singleton"""
        return self.visit_all(node.pattern, inline=True)
    
    def visit_MatchSequence(self, node):
        """Visit match sequence"""
        return self.visit_all(node.pattern, inline=True)
    
    def visit_MatchMapping(self, node):
        """Visit match mapping"""
        return self.visit_all(node.pattern, inline=True)
    
    def visit_MatchClass(self, node):
        """Visit match class"""
        return self.visit_all(node.pattern, inline=True)
    
    def visit_MatchAs(self, node):
        """Visit match as"""
        return self.visit_all(node.pattern, inline=True)
    
    def visit_MatchKeyword(self, node):
        """Visit match keyword"""
        return self.visit_all(node.pattern, inline=True)
    
    def visit_MatchStar(self, node):
        """Visit match star"""
        return self.visit_all(node.pattern, inline=True)
    
    def visit_MatchOr(self, node):
        """Visit match or"""
        return self.visit_all(node.pattern, inline=True)
    
    ### END MATCH ###
    def visit_AsyncWith(self, node):
        """Visit async with"""
        """Visit with"""
        self.emit("coroutine.wrap(function()")
        self.visit_all(node.body)
        body = self.output[-1]
        lines = []
        for i in node.items:
            line = ""
            if i.optional_vars is not None:
                line = "local {} = "
                line = line.format(self.visit_all(i.optional_vars,
                                                  inline=True))
            line += self.visit_all(i.context_expr, inline=True)
            lines.append(line)
        for line in lines:
            body.insert(0, line)
        self.emit("end)()")
        
    def visit_Slice(self, node):
        """Visit slice"""
        error("syntax based slicing is not supported yet. Use slice(<sequence>, <start>, <end>, <step>) instead.")
        
    def visit_JoinedStr(self, node):
        # f"{a} {b}"
        # becomes
        # `{a} {b}`
        
        """Visit joined string"""
        values = []
        for value in node.values:
            if isinstance(value, ast.Str):
                values.append(value.s)
            else:
                values.append(self.visit_all(value, inline=True))
        self.emit("`{}`".format("".join(values)))
        
    def visit_FormattedValue(self, node):
        """Visit formatted value"""
        # f"{a}"
        # becomes
        # {a}
        self.emit("{" + (self.visit_all(node.value, inline=True)) + "}")
    
    def visit_Bytes(self, node):
        """Visit bytes"""
        # Use utf8 strings instead of bytes
        self.emit("\"{}\"".format(node.s.decode("utf8")))
        
        
    def visit_TryStar(self, node):
        """Visit try"""
        self.emit("local success, result = pcall(function()")
        self.visit_all(node.body)
        self.emit("end)")
        
    def visit_Assert(self, node):
        """Visit assert"""
        self.emit("assert({})".format(self.visit_all(node.test, True)))
        
    def visit_Nonlocal(self, node):
        """Visit nonlocal"""
        for name in node.names:
            self.context.last()["nonlocals"].add_symbol(name)
        
    def visit_AnnAssign(self, node): 
        """Visit annassign"""
        target = self.visit_all(node.target, inline=True)
        value = self.visit_all(node.value, inline=True)
        local_keyword = ""
        last_ctx = self.context.last()
        if last_ctx["class_name"]:
            target = ".".join([last_ctx["class_name"], target])
        if "." not in target and not last_ctx["locals"].exists(target):
            local_keyword = "local "
            last_ctx["locals"].add_symbol(target)
        type = self.visit_all(node.annotation, inline=True)
        
        if type == "int" or type == "float":
            type = "number"
        elif type == "str":
            type = "string"
        elif type == "list" or type == "dict" or type == "memoryview" or type == "bytearray" or type == "set" or type == "range" or type == "frozenset" or type == "module" or type == "classobj" or type == "class" or type == "tuple":
            type = "table"
        elif type == "NoneType":
            type = "nil"
        elif type == "ellipsis" or type == "NotImplementedType" or type == "slice" or type == "classmethod" or type == "type" or type == "staticmethod":
            error("The Python type '{}' can not be converted to Luau.".format(type))
            
        if value != None and value != "":
            self.emit("{local}{target}: {type} = {value}".format(local=local_keyword,
                                                        target=target,
                                                        value=value,
                                                        type=type))
        # example input:
        # a: int = 1
        # example output:
        # local a = 1
        
    def visit_AugAssign(self, node):
        """Visit augassign"""
        operation = BinaryOperationDesc.OPERATION[node.op.__class__]

        target = self.visit_all(node.target, inline=True)

        values = {
            "left": target,
            "right": self.visit_all(node.value, inline=True),
            "operation": operation["value"],
        }

        line = "({})".format(operation["format"])
        line = line.format(**values)

        self.emit("{target} = {line}".format(target=target, line=line))

    def visit_Attribute(self, node):
        """Visit attribute"""
        line = "{object}.{attr}"
        values = {
            "object": self.visit_all(node.value, True),
            "attr": node.attr,
        }
        # Does object start and end with a " "
        if (values["object"].startswith('"') and values["object"].endswith('"')) or (values["object"].startswith('\'') and values["object"].endswith('\'')) or (values["object"].startswith('{') and values["object"].endswith('}')) or (values["object"].startswith('[') and values["object"].endswith(']')) or (values["object"].startswith('`') and values["object"].endswith('`')):
            values["object"] = "({})".format(values["object"])
        
        self.emit(line.format(**values))

    def visit_BinOp(self, node):
        """Visit binary operation"""
        operation = BinaryOperationDesc.OPERATION[node.op.__class__]
        line = "({})".format(operation["format"])
        values = {
            "left": self.visit_all(node.left, True),
            "right": self.visit_all(node.right, True),
            "operation": operation["value"],
        }

        self.emit(line.format(**values))

    def visit_BoolOp(self, node):
        """Visit boolean operation"""
        operation = BooleanOperationDesc.OPERATION[node.op.__class__]
        line = "({})".format(operation["format"])
        values = {
            "left": self.visit_all(node.values[0], True),
            "right": self.visit_all(node.values[1], True),
            "operation": operation["value"],
        }

        self.emit(line.format(**values))

    def visit_Break(self, node):
        """Visit break"""
        self.emit("break")

    def visit_Call(self, node):
        """Visit function call"""
        line = "{name}({arguments})"

        name = self.visit_all(node.func, inline=True)
        arguments = [self.visit_all(arg, inline=True) for arg in node.args]

        self.emit(line.format(name=name, arguments=", ".join(arguments)))

    def visit_ClassDef(self, node):
        """Visit class definition"""
        bases = [self.visit_all(base, inline=True) for base in node.bases]

        local_keyword = ""
        last_ctx = self.context.last()
        if not last_ctx["class_name"] and not last_ctx["locals"].exists(node.name):
            local_keyword = "local "
            last_ctx["locals"].add_symbol(node.name)

        name = node.name
        if last_ctx["class_name"]:
            name = ".".join([last_ctx["class_name"], name])

        values = {
            "local": local_keyword,
            "name": name,
            "node_name": node.name,
        }

        self.emit("{local}{name} = class(function({node_name})".format(**values))
        self.depend("class")
        
        self.context.push({"class_name": node.name})
        self.visit_all(node.body)
        self.context.pop()

        self.output[-1].append("return {node_name}".format(**values))

        self.emit("end, {{{}}})".format(", ".join(bases)))

        # Return class object only in the top-level classes.
        # Not in the nested classes.
        if self.config["class"]["return_at_the_end"] and not last_ctx["class_name"]:
            self.emit("return {}".format(name))

    def visit_Compare(self, node):
        """Visit compare"""

        line = ""

        left = self.visit_all(node.left, inline=True)
        for i in range(len(node.ops)):
            operation = node.ops[i]
            operation = CompareOperationDesc.OPERATION[operation.__class__]

            right = self.visit_all(node.comparators[i], inline=True)

            values = {
                "left": left,
                "right": right,
            }

            if isinstance(operation, str):
                values["op"] = operation
                line += "{left} {op} {right}".format(**values)
            elif isinstance(operation, dict):
                line += operation["format"].format(**values)

            if i < len(node.ops) - 1:
                left = right
                line += " and "

        self.emit("({})".format(line))

    def visit_Continue(self, node):
        """Visit continue"""
        last_ctx = self.context.last()
        line = "continue"
        self.emit(line)

    def visit_Delete(self, node):
        """Visit delete"""
        targets = [self.visit_all(target, inline=True) for target in node.targets]
        nils = ["nil" for _ in targets]
        line = "{targets} = {nils}".format(targets=", ".join(targets),
                                           nils=", ".join(nils))
        self.emit(line)

    def visit_Dict(self, node):
        """Visit dictionary"""
        keys = []

        for key in node.keys:
            value = self.visit_all(key, inline=True)
            if isinstance(key, ast.Str):
                value = "[{}]".format(value)
            keys.append(value)

        values = [self.visit_all(item, inline=True) for item in node.values]

        elements = ["{} = {}".format(keys[i], values[i]) for i in range(len(keys))]
        elements = ", ".join(elements)
        self.depend("dict")
        self.emit("dict {{{}}}".format(elements))

    def visit_DictComp(self, node):
        """Visit dictionary comprehension"""
        self.emit("(function()")
        self.depend("dict")
        self.emit("local result = dict {}")

        ends_count = 0

        for comp in node.generators:
            line = "for {target} in {iterator} do"
            values = {
                "target": self.visit_all(comp.target, inline=True),
                "iterator": self.visit_all(comp.iter, inline=True),
            }
            line = line.format(**values)
            self.emit(line)
            ends_count += 1

            for if_ in comp.ifs:
                line = "if {} then".format(self.visit_all(if_, inline=True))
                self.emit(line)
                ends_count += 1

        line = "result[{key}] = {value}"
        values = {
            "key": self.visit_all(node.key, inline=True),
            "value": self.visit_all(node.value, inline=True),
        }
        self.emit(line.format(**values))

        self.emit(" ".join(["end"] * ends_count))

        self.emit("return result")
        self.emit("end)()")

    def visit_Ellipsis(self, node):
        """Visit ellipsis"""
        self.emit("...")

    def visit_Expr(self, node):
        """Visit expr"""
        expr_is_docstring = False
        if isinstance(node.value, ast.Str):
            expr_is_docstring = True

        self.context.push({"docstring": expr_is_docstring})
        output = self.visit_all(node.value)
        self.context.pop()

        self.output.append(output)

    def visit_FunctionDef(self, node):
        """Visit function definition"""
        line = "{local}function {name}({arguments})"

        last_ctx = self.context.last()

        name = node.name
        type = 1 # 1 = static, 2 = class
        for decorator in reversed(node.decorator_list):
            decorator_name = self.visit_all(decorator, inline=True)
            
            if decorator_name == "classmethod":
                type = 2
            elif decorator_name == "staticmethod":
                type = 1
        if last_ctx["class_name"]:
            name = ".".join([last_ctx["class_name"], name])
            
        if type == 1:
            arguments = [arg.arg for arg in node.args.args]
        else:
            arguments = ["self"]
            arguments.extend([arg.arg for arg in node.args.args])

        if node.args.vararg is not None:
            arguments.append("...")

        local_keyword = ""

        if "." not in name and not last_ctx["locals"].exists(name):
            local_keyword = "local "
            last_ctx["locals"].add_symbol(name)

        function_def = line.format(local=local_keyword,
                                   name=name,
                                   arguments=", ".join(arguments))

        self.emit(function_def)

        self.context.push({"class_name": ""})
        self.visit_all(node.body)
        self.context.pop()

        body = self.output[-1]

        if node.args.vararg is not None:
            self.depend("list")
            line = "local {name} = list({{...})".format(name=node.args.vararg.arg)
            body.insert(0, line)

        arg_index = -1
        for i in reversed(node.args.defaults):
            line = "{name} = {name} or {value}"

            arg = node.args.args[arg_index]
            values = {
                "name": arg.arg,
                "value": self.visit_all(i, inline=True),
            }
            body.insert(0, line.format(**values))

            arg_index -= 1

        self.emit("end")

        for decorator in reversed(node.decorator_list):
            decorator_name = self.visit_all(decorator, inline=True)
            if decorator_name == "classmethod" or decorator_name == "staticmethod":
                continue
            values = {
                "name": name,
                "decorator": decorator_name,
            }
            line = "{name} = {decorator}({name})".format(**values)
            self.emit(line)

    def visit_For(self, node):
        """Visit for loop"""
        line = "for {target} in {iter} do"

        values = {
            "target": self.visit_all(node.target, inline=True),
            "iter": self.visit_all(node.iter, inline=True),
        }

        self.emit(line.format(**values))

        continue_label = LoopCounter.get_next()
        self.context.push({
            "loop_label_name": continue_label,
        })
        self.visit_all(node.body)
        self.context.pop()

        self.emit("end")

    def visit_Global(self, node):
        """Visit globals"""
        last_ctx = self.context.last()
        for name in node.names:
            last_ctx["globals"].add_symbol(name)

    def visit_AsyncFunctionDef(self, node):
        """Visit async function definition"""
        line = "{local}function {name}({arguments}) coroutine.wrap(function()"

        last_ctx = self.context.last()

        name = node.name
        if last_ctx["class_name"]:
            name = ".".join([last_ctx["class_name"], name])

        arguments = [arg.arg for arg in node.args.args]

        if node.args.vararg is not None:
            arguments.append("...")

        local_keyword = ""

        if "." not in name and not last_ctx["locals"].exists(name):
            local_keyword = "local "
            last_ctx["locals"].add_symbol(name)

        function_def = line.format(local=local_keyword,
                                   name=name,
                                   arguments=", ".join(arguments))

        self.emit(function_def)

        self.context.push({"class_name": ""})
        self.visit_all(node.body)
        self.context.pop()

        body = self.output[-1]

        if node.args.vararg is not None:
            line = "local {name} = list {{...}}".format(name=node.args.vararg.arg)
            body.insert(0, line)

        arg_index = -1
        for i in reversed(node.args.defaults):
            line = "{name} = {name} or {value}"

            arg = node.args.args[arg_index]
            values = {
                "name": arg.arg,
                "value": self.visit_all(i, inline=True),
            }
            body.insert(0, line.format(**values))

            arg_index -= 1

        self.emit("end)() end")

        for decorator in reversed(node.decorator_list):
            decorator_name = self.visit_all(decorator, inline=True)
            values = {
                "name": name,
                "decorator": decorator_name,
            }
            line = "{name} = {decorator}({name})".format(**values)
            self.emit(line)
        
    def visit_Await(self, node):
        """Visit await"""
        self.emit("coroutine.await({})".format(self.visit_all(node.value, inline=True)))
        
    def visit_Yield(self, node):
        """Visit yield"""
        self.emit("coroutine.yield({})".format(self.visit_all(node.value, inline=True)))
        
    def visit_If(self, node):
        """Visit if"""
        test = self.visit_all(node.test, inline=True)

        line = "if {} then".format(test)

        self.emit(line)
        self.visit_all(node.body)

        if node.orelse:
            if isinstance(node.orelse[0], ast.If):
                elseif = node.orelse[0]
                elseif_test = self.visit_all(elseif.test, inline=True)

                line = "elseif {} then".format(elseif_test)
                self.emit(line)

                output_length = len(self.output)
                self.visit_If(node.orelse[0])

                del self.output[output_length]
                del self.output[-1]
            else:
                self.emit("else")
                self.visit_all(node.orelse)

        self.emit("end")

    def visit_IfExp(self, node):
        """Visit if expression"""
        line = "{cond} and {true_cond} or {false_cond}"
        values = {
            "cond": self.visit_all(node.test, inline=True),
            "true_cond": self.visit_all(node.body, inline=True),
            "false_cond": self.visit_all(node.orelse, inline=True),
        }

        self.emit(line.format(**values))

    def visit_Import(self, node):
        """Visit import"""
        line = 'local {asname} = require("{name}")'
        values = {"asname": "", "name": ""}

        if node.names[0].asname is None:
            values["name"] = node.names[0].name
            values["asname"] = values["name"]
            values["asname"] = values["asname"].split(".")[-1]
        else:
            values["asname"] = node.names[0].asname
            values["name"] = node.names[0].name

        self.emit(line.format(**values))
    
    def visit_ImportFrom(self, node):
        """Visit import from"""
        module = node.module
        if module is None:
            module = ""
        else:
            module = module

        for name in node.names:
            if name.asname is None:
                if name.name == "*":
                    error("import * is unsupproted")
                else:
                    self.emit("local {name} = require(\"{module}\").{name}".format(
                        name=name.name,
                        module=module,
                    ))
            else:
                if name.name == "*":
                    error("import * is unsupproted")
                else:
                    self.emit("local {name} = require(\"{module}\").{realname}".format(
                        name=name.asname,
                        module=module,
                        realname=name.name,
                    ))

    def visit_Index(self, node):
        """Visit index"""
        self.emit(self.visit_all(node.value, inline=True))

    def visit_Lambda(self, node):
        """Visit lambda"""
        line = "function({arguments}) return"

        arguments = [arg.arg for arg in node.args.args]

        function_def = line.format(arguments=", ".join(arguments))

        output = []
        output.append(function_def)
        output.append(self.visit_all(node.body, inline=True))
        output.append("end")

        self.emit(" ".join(output))

    def visit_List(self, node):
        """Visit list"""
        elements = [self.visit_all(item, inline=True) for item in node.elts]
        line = "list {{{}}}".format(", ".join(elements))
        self.emit(line)

    def visit_ListComp(self, node):
        """Visit list comprehension"""
        self.emit("(function()")
        self.emit("local result = list {}")

        ends_count = 0

        for comp in node.generators:
            line = "for {target} in {iterator} do"
            values = {
                "target": self.visit_all(comp.target, inline=True),
                "iterator": self.visit_all(comp.iter, inline=True),
            }
            line = line.format(**values)
            self.emit(line)
            ends_count += 1

            for if_ in comp.ifs:
                line = "if {} then".format(self.visit_all(if_, inline=True))
                self.emit(line)
                ends_count += 1

        line = "result.append({})"
        line = line.format(self.visit_all(node.elt, inline=True))
        self.emit(line)

        self.emit(" ".join(["end"] * ends_count))

        self.emit("return result")
        self.emit("end)()")

    def visit_Module(self, node):
        """Visit module"""
        self.visit_all(node.body)
        self.output = self.output[0]

    def visit_Name(self, node):
        """Visit name"""
        self.emit(node.id)

    def visit_NameConstant(self, node):
        """Visit name constant"""
        self.emit(NameConstantDesc.NAME[node.value])

    def visit_Num(self, node):
        """Visit number"""
        self.emit(str(node.n))

    def visit_Pass(self, node):
        """Visit pass"""
        pass

    def visit_Return(self, node):
        """Visit return"""
        line = "return "
        line += self.visit_all(node.value, inline=True)
        self.emit(line)

    def visit_Starred(self, node):
        """Visit starred object"""
        value = self.visit_all(node.value, inline=True)
        line = "unpack({})".format(value)
        self.emit(line)

    def visit_Str(self, node):
        """Visit str"""
        value = node.s
        if value.startswith(NodeVisitor.LUACODE):
            value = value[len(NodeVisitor.LUACODE):]
            self.emit(value)
        elif self.context.last()["docstring"]:
            self.emit('--[[ {} ]]'.format(node.s))
        else:
            self.emit('"{}"'.format(node.s))

    def visit_Subscript(self, node):
        """Visit subscript"""
        line = "{name}[{index}]"
        values = {
            "name": self.visit_all(node.value, inline=True),
            "index": self.visit_all(node.slice, inline=True),
        }

        self.emit(line.format(**values))

    def visit_Tuple(self, node):
        """Visit tuple"""
        elements = [self.visit_all(item, inline=True) for item in node.elts]
        self.emit(", ".join(elements))

    def visit_UnaryOp(self, node):
        """Visit unary operator"""
        operation = UnaryOperationDesc.OPERATION[node.op.__class__]
        value = self.visit_all(node.operand, inline=True)

        line = operation["format"]
        values = {
            "value": value,
            "operation": operation["value"],
        }

        self.emit(line.format(**values))
    
    def visit_Raise(self, node):
        """Visit raise"""
        line = "error({})".format(self.visit_all(node.exc, inline=True))
        self.emit(line)
        
    def visit_Set(self, node):
        """Visit set"""
        values = [self.visit_all(value, True) for value in node.elts]
        self.emit('{' + ', '.join(values) + '}')
        
    def visit_Try(self, node):
        """Visit try"""
        self.emit("xpcall(function()")

        self.visit_all(node.body)
        
        self.emit("end, function(err)")
        
        self.visit_all(node.handlers)
        
        self.emit("end)")
        
    def visit_ExceptHandler(self, node):
        """Visit exception handler"""
        self.emit("if err:find('{}') then".format(node.type.id))
        
        self.visit_all(node.body)
        
        self.emit("end")
        
    def visit_While(self, node):
        """Visit while"""
        test = self.visit_all(node.test, inline=True)

        self.emit("while {} do".format(test))

        continue_label = LoopCounter.get_next()
        self.context.push({
            "loop_label_name": continue_label,
        })
        self.visit_all(node.body)
        self.context.pop()

        self.emit("end")

    
    def visit_SetComp(self, node):
        """Visit set comprehension"""
        self.emit("(function()")
        self.emit("local result = {}")
        ends_count = 0
        for comp in node.generators:
            line = "for {target} in {iterator} do"
            values = {
                "target": self.visit_all(comp.target, inline=True),
                "iterator": self.visit_all(comp.iter, inline=True),
            }
            line = line.format(**values)
            self.emit(line)
            ends_count += 1
            for if_ in comp.ifs:
                line = "if {} then".format(self.visit_all(if_, inline=True))
                self.emit(line)
                ends_count += 1
        line = "table.insert(result, {})"
        line = line.format(self.visit_all(node.elt, inline=True))
        self.emit(line)
        self.emit(" ".join(["end"] * ends_count))
        self.emit("return result")
        self.emit("end)()")
        
    def visit_With(self, node):
        """Visit with"""
        self.emit("do")

        self.visit_all(node.body)

        body = self.output[-1]
        lines = []
        for i in node.items:
            line = ""
            if i.optional_vars is not None:
                line = "local {} = "
                line = line.format(self.visit_all(i.optional_vars,
                                                  inline=True))
            line += self.visit_all(i.context_expr, inline=True)
            lines.append(line)

        for line in lines:
            body.insert(0, line)

        self.emit("end")

    def generic_visit(self, node):
        """Unknown nodes handler"""
        if node is None:
            return
        error("Unsupported feature: '{}'".format(node.__class__.__name__))

    def visit_all(self, nodes, inline=False):
        """Visit all nodes in the given list"""

        if not inline:
            last_ctx = self.context.last()
            last_ctx["locals"].push()

        visitor = NodeVisitor(context=self.context, config=self.config)

        if isinstance(nodes, list):
            for node in nodes:
                visitor.visit(node)
            if not inline:
                self.output.append(visitor.output)
        else:
            visitor.visit(nodes)
            if not inline:
                self.output.extend(visitor.output)

        if not inline:
            last_ctx = self.context.last()
            last_ctx["locals"].pop()

        if inline:
            return " ".join(visitor.output)

    def emit(self, value):
        """Add translated value to the output"""
        self.output.append(value)
    def depend(self, value):
        """Add dependency value to the object"""
        dependencies.append(value)
        
"""Header"""
HEADER = f"--// Generated by roblox-py v{VERSION} \\\\--\n"
PY_HEADER = f"## Generated by roblox-py v{VERSION} ##\n"

"""Python to lua translator class"""
class Translator:
    """Python to lua main class translator"""
    def __init__(self, config=None, show_ast=False):
        self.config = config if config is not None else Config()
        self.show_ast = show_ast

        self.output = []

    def translate(self, pycode):
        """Translate python code to lua code"""
        try:
            # code that uses ast
            py_ast_tree = ast.parse(pycode)
        except SyntaxError as err:
            sys.stderr.write("\033[1;31m" + "syntax error: " + "\033[0m" + str(err) + "\n")
            sys.exit(1)
            
        visitor = NodeVisitor(config=self.config)

        if self.show_ast:
            print(ast.dump(py_ast_tree))

        visitor.visit(py_ast_tree)
        
        DEPEND = "\n\n--// REQUIREMENTS \\\\--\n"
        
        self.output = visitor.output
        
        for depend in dependencies:
            # set
            
            if depend == "list":
                DEPEND += """function list(t)
	local result = {}

	result._is_list = true

	result._data = {}
	for _, v in ipairs(t) do
		table.insert(result._data, v)
	end

	local methods = {}

	methods.append = function(value)
		table.insert(result._data, value)
	end

	methods.extend = function(iterable)
		for value in iterable do
			table.insert(result._data, value)
		end
	end

	methods.insert = function(index, value)
		table.insert(result._data, index, value)
	end

	methods.remove = function(value)
		for i, v in ipairs(result._data) do
			if value == v then
				table.remove(result._data, i)
				break
			end
		end
	end

	methods.pop = function(index)
		index = index or #result._data
		local value = result._data[index]
		table.remove(result._data, index)
		return value
	end

	methods.clear = function()
		result._data = {}
	end

	methods.index = function(value, start, end_)
		start = start or 1
		end_ = end_ or #result._data

		for i = start, end_, 1 do
			if result._data[i] == value then
				return i
			end
		end

		return nil
	end

	methods.count = function(value)
		local cnt = 0
		for _, v in ipairs(result._data) do
			if v == value then
				cnt = cnt + 1
			end
		end

		return cnt
	end

	methods.sort = function(key, reverse)
		key = key or nil
		reverse = reverse or false

		table.sort(result._data, function(a, b)
			if reverse then
				return a < b
			end

			return a > b
		end)
	end

	methods.reverse = function()
		local new_data = {}
		for i = #result._data, 1, -1 do
			table.insert(new_data, result._data[i])
		end

		result._data = new_data
	end

	methods.copy = function()
		return list(result._data)
	end

	local iterator_index = nil

	setmetatable(result, {
		__index = function(self, index)
			if typeof(index) == "number" then
				if index < 0 then
					index = #result._data + index
				end
				return rawget(result._data, index + 1)
			end
			return methods[index]
		end,
		__newindex = function(self, index, value)
			result._data[index] = value
		end,
		__call = function(self, _, idx)
			if idx == nil and iterator_index ~= nil then
				iterator_index = nil
			end

			local v = nil
			iterator_index, v = next(result._data, iterator_index)

			return v
		end,
	})

	return result
end"""
            elif depend == "dict":
                DEPEND += """function dict(t)
	local result = {}

	result._is_dict = true

	result._data = {}
	for k, v in pairs(t) do
		result._data[k] = v
	end

	local methods = {}

	local key_index = nil

	methods.clear = function()
		result._data = {}
	end

	methods.copy = function()
		return dict(result._data)
	end

	methods.get = function(key, default)
		default = default or nil
		if result._data[key] == nil then
			return default
		end

		return result._data[key]
	end

	methods.items = function()
		return pairs(result._data)
	end

	methods.keys = function()
		return function(self, idx, _) 
			if idx == nil and key_index ~= nil then
				key_index = nil
			end

			key_index, _ = next(result._data, key_index)
			return key_index
		end
	end

	methods.pop = function(key, default)
		default = default or nil
		if result._data[key] ~= nil then
			local value = result._data[key]
			result._data[key] = nil 
			return key, value
		end

		return key, default
	end

	methods.popitem = function()
		local key, value = next(result._data)
		if key ~= nil then
			result._data[key] = nil
		end

		return key, value
	end

	methods.setdefault = function(key, default)
		if result._data[key] == nil then
			result._data[key] = default
		end

		return result._data[key]
	end

	methods.update = function(t)
		assert(t._is_dict)

		for k, v in t.items() do
			result._data[k] = v
		end
	end

	methods.values = function()
		return function(self, idx, _) 
			if idx == nil and key_index ~= nil then
				key_index = nil
			end

			key_index, value = next(result._data, key_index)
			return value
		end
	end

	setmetatable(result, {
		__index = function(self, index)
			if typeof(index) == "string" then
				-- If it starts with SLICE! then it is a slice, get the start, stop, and step values. Sometimes the 3rd value is not there, so we need to check for that
				if string.sub(index, 1, 6) == "SLICE!" then
					local start, stop, step = string.match(index, "SLICE!%((%d+), (%d+), (%d+)%)")
					if (not stop) and (not step) and start then -- 1 value
						start = string.match(index, "SLICE!%((%d+), (%d+)%)")
						step = 1
						stop = -1
					elseif not step then -- 2 values
						start, stop = string.match(index, "SLICE!%((%d+), (%d+)%)")
						step = 1
					end
					return slicefun(self, tonumber(start), tonumber(stop), tonumber(step))
				end
			end
			if result._data[index] ~= nil then
				return result._data[index]
			end
			return methods[index]
		end,
		__newindex = function(self, index, value)
			result._data[index] = value
		end,
		__call = function(self, _, idx)
			if idx == nil and key_index ~= nil then
				key_index = nil
			end

			key_index, _ = next(result._data, key_index)

			return key_index            
		end,
	})

	return result
end"""
            elif depend == "class":
                DEPEND += """function class(class_init, bases)
    bases = bases or {}

    local c = {}

    for _, base in ipairs(bases) do
        for k, v in pairs(base) do
            c[k] = v
        end
    end

    c._bases = bases

    c = class_init(c)

    local mt = getmetatable(c) or {}
    mt.__call = function(_, ...)
        local object = {}

        setmetatable(object, {
            __index = function(tbl, idx)
                local method = c[idx]
                if typeof(method) == "function" then
                    return function(...)
                        return c[idx](object, ...) 
                    end
                end

                return method
            end,
        })

        if typeof(object.__init__) == "function" then
            object.__init__(...)
        end

        return object
    end

    setmetatable(c, mt)

    return c
end"""
            #elif depend == "set":
            #    pass
            else:
                error("Auto-generated dependency unhandled {}, please report this issue on Discord or Github".format(depend))

                    
        DEPEND += "\n\n----- CODE START -----\n"
        

        return HEADER + DEPEND + self.to_code()

    def to_code(self, code=None, indent=0):
        """Create a lua code from the compiler output"""
        code = code if code is not None else self.output

        def add_indentation(line):
            """Add indentation to the given line"""
            indentation_width = 4
            indentation_space = " "

            indent_copy = max(indent, 0)

            return indentation_space * indentation_width * indent_copy + line

        lines = []
        for line in code:
            if isinstance(line, str):
                lines.append(add_indentation(line))
            elif isinstance(line, list):
                sub_code = self.to_code(line, indent + 1)
                lines.append(sub_code)

        return "\n".join(lines)

    @staticmethod
    def get_luainit(): # Return STDlib
        return """"""

""" Lua Lexer """
# Convert source to tokens
def is_operator(char):
    return char in [
        "~=", "=", "==", "(", ")", "<", "+", "-", "*", ">", "<", "not", "%",
        "/", "{", "}", ",", "[", "]", "#"
    ]


KEYWORDS = [
    "while", "do", "end", "if", "elseif", "else", "then", "function", "return",
    "for", "in",
]


def is_keyword(word):
    return word in KEYWORDS


def is_letter(char):
    return re.search(r'[a-zA-Z]|_', char)


def is_num(char):
    return re.search(r'[0-9]', char)


def extract_operator(chars):
    op = ""
    for letter in chars:
        if not is_operator(op+letter):
            break

        op = op+letter
    del chars[0:len(op)]
    return op


def extract_num(chars):
    num = ""

    for letter in chars:
        if not is_num(letter) and letter != ".":
            break

        num = num+letter
    del chars[0:len(num)]
    return num


def extract_str(indicator, chars):
    out = ""
    for letter in chars[1:]:
        if letter == indicator:
            break

        out = out+letter
    del chars[0:len(out)+2]
    return out


def extract_word(chars):
    word = ""
    for letter in chars:
        if not is_letter(letter) and not re.search(r'([0-9]|_)', letter):
            break

        word = word+letter
    del chars[0:len(word)]
    return word


def extract_multiline_comment(chars):
    string_chars = "".join(chars)
    end_index = string_chars.index("--]]")

    val = string_chars[0:end_index]
    del chars[0:end_index+4]
    return val


def extract_comment(chars):
    string_chars = "".join(chars)
    end_index = string_chars.index("\n")

    val = string_chars[2:end_index]
    del chars[0:end_index]
    return val


def extract_multiline_str(chars):
    string_chars = "".join(chars)
    end_index = string_chars.index("]]")

    val = string_chars[2:end_index]
    del chars[0:end_index+2]
    return val

def lexer(source):
    chars = list(source)
    tokens = []

    while len(chars):
        char = chars[0]

        if char == "\n":
            char = chars.pop(0)
            tokens.append({"type": "NL"})
            continue

        if chars[0:4] == ["-", "-", "[", "["]:
            comment = extract_multiline_comment(chars)
            tokens.append({"type": "MULTI-COMMENT", "value": comment})
            continue

        if chars[0:3] == ['n', 'i', 'l']:
            tokens.append({"type": "NIL", "value": 'nil'})
            del chars[0:3]
            continue

        if chars[0:2] == ["-", "-"]:
            comment = extract_comment(chars)
            tokens.append({"type": "COMMENT", "value": comment})
            continue

        if chars[0:3] == ["a", "n", "d"]:
            tokens.append({"type": "OP", "value": "and"})
            del chars[0:3]
            continue

        if chars[0:2] == ["o", "r"]:
            tokens.append({"type": "OP", "value": "or"})
            del chars[0:2]
            continue

        if chars[0:3] == ["n", "o", "t"]:
            tokens.append({"type": "OP", "value": "not"})
            del chars[0:3]
            continue

        if chars[0:2] == ["~", "="]:
            tokens.append({"type": "OP", "value": "~="})
            del chars[0:2]
            continue

        if chars[0:2] == [".", "."]:
            tokens.append({"type": "OP", "value": ".."})
            del chars[0:2]
            continue

        if chars[0:2] == [">", "="]:
            tokens.append({"type": "OP", "value": ">="})
            del chars[0:2]
            continue

        if chars[0:2] == ["<", "="]:
            tokens.append({"type": "OP", "value": "<="})
            del chars[0:2]
            continue

        if len(chars) >= 2 and char == "-" and is_num(chars[1]):
            del chars[0:1]
            num = "-"+extract_num(chars)
            tokens.append({"type": "NUMBER", "value": num})
            continue

        if is_num(char):
            num = extract_num(chars)
            tokens.append({"type": "NUMBER", "value": num})
            continue

        if is_operator(char):
            operator = extract_operator(chars)
            tokens.append({"type": "OP", "value": operator})
            continue

        if char == "'":
            string = extract_str("'", chars)
            tokens.append({"type": "STRING", "value": string})
            continue

        if char == '"':
            string = extract_str('"', chars)
            tokens.append({"type": "STRING", "value": string})
            continue

        if chars[0:2] == ["[", "["]:
            comment = extract_multiline_str(chars)
            tokens.append({"type": "STRING", "value": comment})
            continue

        if is_letter(char):
            word = extract_word(chars)
            if is_keyword(word):
                tokens.append({"type": "KEYWORD", "value": word})
                continue

            if word in ["true", "false"]:
                tokens.append({"type": "BOOLEAN", "value": word})
                continue

            tokens.append({"type": "NAME", "value": word})
            continue

        chars.pop(0)

    return tokens

""" Lua Parser """
# Covert tokens to AST

OPERATORS = [
    "+", "-", "=", "*", ">", "<", "~=", "==", "..", ">=", "<=", "%", "/", "and", "or",
]

fn_name_index = 0


def generate_function_name():
    global fn_name_index

    fn_name_index = fn_name_index + 1
    return "__fn{0}".format(fn_name_index)


def parse_tokens(tokens, in_body=0, in_table_construct=0, in_fn_arguments=0):

    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        # Make sure we do not construct tuple when comma list is passed
        # as function arguments/table constructor
        if len(tokens) \
                and is_op(tokens[0], ",") \
                and in_fn_arguments == 0 \
                and in_table_construct == 0:

            tuple_tokens = [token]
            tokens.pop(0)

            # Continue through comma list until the end
            while len(tokens) > 0:
                tuple_tokens.append(tokens.pop(0))

                if len(tokens) == 0:
                    break

                if not is_op(tokens[0], ","):
                    break

                tokens.pop(0)

            out.append({"type": "tuple", "value": parse_tokens(tuple_tokens)})
            continue

        if token["type"] == "NUMBER":
            out.append({"type": "number", "value": token["value"]})
            continue

        if token["type"] == "STRING":
            out.append({"type": "string", "value": token["value"]})
            continue

        if token["type"] == "BOOLEAN":
            out.append({"type": "boolean", "value": token["value"]})
            continue

        if token["type"] == "NIL":
            out.append({"type": "nil", "value": None})
            continue

        if token["type"] == "OP" and token["value"] == "#":
            assignments = extract_assignments(tokens)
            out.append({
                "type": "call",
                "name": "#",
                "args": parse_tokens(assignments),
            })
            continue

        if token["type"] == "OP" and token["value"] == "{":
            table_tokens = extract_table(tokens)
            table_tokens = extract_assignments_by_comma(table_tokens)

            nodes = map(
                lambda x: parse_tokens(x, in_table_construct=1),
                table_tokens
            )

            nodes = [x[0] for x in nodes]

            # print(table_tokens)
            out.append({
                "type": "table",
                "value": nodes,
            })
            continue

        if token["type"] == "OP" and token["value"] == "not":
            assignments = extract_assignments(tokens)
            out.append({
                "type": "call",
                "name": token["value"],
                "args": parse_tokens(assignments),
            })
            continue

        # Ignore [ if beeing used as constructor in table
        if in_table_construct == 1 and is_op(token, "["):
            continue

        # [ is beeing used as a accessor for table
        if in_table_construct == 0 and is_op(token, "["):
            key_tokens = extract_until_end_op(tokens, "]")

            expression = {
                "type": "call",
                "name": "[",
                "args": [out.pop(), parse_tokens(key_tokens)],
            }

            if in_body:  # Do not wrap expression if already running in one
                out.append({
                    "type": "expr",
                    "value": [expression],
                })
            else:
                out.append(expression)
            continue

        if token["type"] == "OP" and token["value"] in OPERATORS:
            assignments = extract_assignments(tokens)

            # Move function outside assignment and declare it in above scope
            # with keyword ref
            if token["value"] == "=" and is_lex_keyword(assignments[0], "function"):
                assignments = inline_anonymous_function(assignments, out)

            out.append({
                "type": "call",
                "name": token["value"],
                "args": [
                    out.pop(),
                    parse_tokens(
                        assignments,
                        in_table_construct=in_table_construct,
                    )
                ],
            })
            continue

        if token["type"] == "NAME" and len(tokens) and is_op(tokens[0], "("):
            args = extract_args(tokens)

            expression = {
                "type": "call",
                "name": token["value"],
                "args": parse_tokens(args, in_fn_arguments=1)
            }

            if in_body:  # Do not wrap expression if already running in one
                out.append({
                    "type": "expr",
                    "value": [expression],
                })
            else:
                out.append(expression)

            continue

        if token["type"] == "KEYWORD" and token["value"] == "else":
            body = extract_if_body(tokens)

            out.append({
                "type": "else",
                "body": parse_tokens(body, in_body=1),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] in ["if", "elseif"]:
            if_nodes = extract_scope_body(tokens)

            test_nodes = extract_to_keyword(if_nodes, "then")
            body = extract_if_body(if_nodes)

            out.append({
                "type": "if",
                "test": parse_tokens(test_nodes),
                "body": parse_tokens(body, in_body=1),
                "else": parse_tokens(if_nodes),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "for":


            body_tokens = extract_scope_body(tokens)
            iteration_tokens = extract_to_keyword(body_tokens, "do")
            if contains_op(iteration_tokens, "="):
                target_tokens = extract_to_op(iteration_tokens, "=")
            else:
                target_tokens = extract_to_keyword(iteration_tokens, "in")

            out.append({
                "type": "for",
                "target": parse_tokens(target_tokens),
                "iteration": parse_tokens(iteration_tokens),
                "body": parse_tokens(body_tokens, in_body=1),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "while":
            while_tokens = extract_scope_body(tokens)
            test_tokens = extract_to_keyword(while_tokens, "do")

            out.append({
                "type": "while",
                "test": parse_tokens(test_tokens),
                "body": parse_tokens(while_tokens, in_body=1),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "return":
            assignments = extract_assignments(tokens)

            if is_lex_keyword(assignments[0], "function"):
                assignments = inline_anonymous_function(assignments, out)

            out.append({
                "type": "return",
                "value": parse_tokens(assignments),
            })
            continue

        if token["type"] == "KEYWORD" and token["value"] == "function":
            function_tokens = extract_scope_body(tokens)
            signature_tokens = extract_fn_signature(function_tokens)
            function_name = ""

            if signature_tokens[0]["type"] == "NAME":
                name_token = signature_tokens.pop(0)
                function_name = name_token["value"]
            else:
                function_name = None

            parameter_tokens = signature_tokens[1:-1]
            # Only accept name as argument
            parameter_tokens = filter(
                lambda x: x["type"] == "NAME",
                parameter_tokens
            )

            parameter_tokens = map(
                lambda x: {"type": "argument", "name": x["value"]},
                parameter_tokens
            )

            out.append({
                "type": "function",
                "name": function_name,
                "args": list(parameter_tokens),
                "body": parse_tokens(function_tokens, in_body=1),
            })
            continue

        if token["type"] == "NAME":
            out.append({
                "type": "name",
                "name": token["value"],
            })
            continue

    return out


def is_op(token, op):
    return token.get("type", None) == "OP" and token["value"] == op


def is_lex_keyword(token, keyword):
    return token["type"] == "KEYWORD" and token["value"] == keyword


def extract_table(tokens):
    out = []
    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)
        out.append(token)

        if depth > 0 and is_op(token, "}"):
            depth = depth +1
            continue

        if is_op(token, "}"):
            break

    return out


def extract_fn_signature(tokens):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)
        out.append(token)
        if is_op(token, ")"):
            break
    return out


def extract_scope_body(tokens):
    out = []

    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)
        out.append(token)

        if token["type"] == "KEYWORD" and token["value"] in ["if", "function"]:
            depth = depth + 1
            continue

        if depth > 0 and token["type"] == "KEYWORD" and token["value"] in ["if", "end"]:
            depth = depth - 1
            continue

        if depth == 0 and token["type"] == "KEYWORD" and token["value"] == "end":
            break

    return out


def extract_if_body(tokens):
    out = []
    depth = 0

    while len(tokens) > 0:
        token = tokens[0]

        if is_lex_keyword(token, "if"):
            out.append(token)
            tokens.pop(0)
            depth = depth + 1
            continue

        if depth > 0 and is_lex_keyword(token, "end"):
            out.append(token)
            tokens.pop(0)
            depth = depth - 1
            continue

        if depth == 0 and is_lex_keyword(token, "elseif"):
            break

        if depth == 0 and is_lex_keyword(token, "else"):
            break

        if depth == 0 and is_lex_keyword(token, "end"):
            break

        out.append(token)
        tokens.pop(0)

    return out

def extract_until_end_op(tokens, exit_op="]"):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_op(token, exit_op):
            break

        out.append(token)

    return out

def extract_until_end_op(tokens, exit_op="]"):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_op(token, exit_op):
            break

        out.append(token)

    return out


def extract_to_op(tokens, exit_op="="):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_op(token, exit_op):
            break

        out.append(token)

    return out

def extract_to_keyword(tokens, exit_keyword="then"):
    out = []

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_lex_keyword(token, exit_keyword):
            break

        out.append(token)

    return out


def extract_assignments(tokens):
    out = []
    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_lex_keyword(token, "function"):
            out.append(token)
            depth = depth + 1
            continue

        if is_op(token, "("):
            out.append(token)
            depth = depth + 1
            continue

        if is_op(token, "{"):
            out.append(token)
            depth = depth + 1
            continue

        if is_op(token, ")"):
            out.append(token)
            depth = depth - 1
            continue

        if is_lex_keyword(token, "end"):
            out.append(token)
            depth = depth - 1
            continue

        if is_op(token, "}"):
            out.append(token)
            depth = depth - 1
            continue

        if token["type"] == "NL" and depth == 0:
            break

        out.append(token)

    return out

def inline_anonymous_function(tokens, out):
    fn_name = generate_function_name()

    fn_tokens = parse_tokens(tokens)
    fn_tokens[0]["name"] = fn_name
    out.insert(-1, fn_tokens[0])
    assignments = [{"type": "NAME", "value": fn_name}]
    return assignments


def extract_args(tokens):
    depth = 1
    args = []

    tokens.pop(0)  # Drop (

    while depth != 0:
        token = tokens.pop(0)

        if is_op(token, "("):
            depth = depth+1

        if is_op(token, ")"):
            depth = depth-1

        args.append(token)

    args = args[:-1]  # Drop )
    return args


def extract_assignments_by_comma(tokens):
    pairs = [[]]
    depth = 0

    while len(tokens) > 0:
        token = tokens.pop(0)

        if is_op(token, "{"):
            depth = depth + 1

        if is_op(token, "("):
            depth = depth + 1

        if is_op(token, "}"):
            depth = depth - 1

        if is_op(token, ")"):
            depth = depth - 1

        if depth == 0 and is_op(token, ","):
            pairs.append([])
            continue

        pairs[-1].append(token)

    return pairs


def contains_op(tokens, op):
    for token in tokens:
        if is_op(token, op):
            return True
    return False


def parse(tokens):
    ast_ = parse_tokens(tokens, in_body=1)
    return ast_

""" Python Generator """

def ast_to_py_ast(nodes):
    ast_ = parse_nodes(nodes)

    bootstrap = []

    ast_ = bootstrap + ast_

    tree = ast.Module(ast_, [])
    tree = ast.fix_missing_locations(tree)

    return tree


def parse_nodes(nodes, ctx_klass=ast.Load):
    out = []
    while len(nodes) > 0:
        node = nodes.pop(0)

        if node["type"] == "name" and node["name"] == "_G":
            out.append(
                ast.Call(
                    func=ast.Name(id='globals', ctx=ast.Load()),
                    args=[],
                    keywords=[],
                )
            )
            continue

        if node["type"] == "tuple":
            expressions = parse_nodes(node["value"], ctx_klass=ctx_klass)

            out.append(
                ast.Tuple(
                    elts=expressions,
                    ctx=ctx_klass(),
                )
            )
            continue

        if node["type"] == "table":
            argument_nodes = []
            keyword_nodes = []

            for x in node["value"]:
                if not (x["type"] == "call" and x["name"] == "="):
                    argument_nodes.append(x)
                    continue

                keyword_nodes.append(x)

            key_nodes = [x["args"][0] for x in keyword_nodes]
            # Convert name references to strings
            key_nodes = [
                {"type": "string", "value": x["name"]}
                    if x["type"] == "name" else x
                for x in key_nodes
            ]

            value_nodes = [x["args"][1] for x in keyword_nodes]
            value_nodes = [x[0] for x in value_nodes]
            value_nodes = parse_nodes(value_nodes)

            keywords = []
            for x in (zip(key_nodes, value_nodes)):
                name_node, value_node = x
                name = name_node["value"]

                # Apply __ to make sure its casted in Table
                if name_node["type"] == "number":
                    name = "__{0}".format(name)

                keywords.append(
                    ast.keyword(arg=name, value=value_node)
                )

            out.append(
                ast.Call(
                    func=ast.Name(id='Table', ctx=ast.Load()),
                    args=parse_nodes(argument_nodes),
                    keywords=keywords,
                )
            )
            continue

        if node["type"] == "string":
            out.append(ast.Str(s=node["value"]))
            continue

        if node["type"] == "boolean":
            value = node["value"]
            value = True if value == "true" else value
            value = False if value == "false" else value
            out.append(ast.NameConstant(value=value))
            continue

        if node["type"] == "number":
            value = node["value"]
            value = float(value) if "." in value else int(value)

            out.append(ast.Num(n=value))
            continue

        if node["type"] == "nil":
            out.append(ast.NameConstant(value=None))
            continue

        if node["type"] == "return":
            out.append(
                ast.Return(value=parse_nodes(node["value"])[0])
            )
            continue

        if node["type"] == "assign":
            out.append(
                ast.Assign(
                    targets=[
                        ast.Name(id=node["name"], ctx=ast.Store())
                    ],
                    value=parse_nodes(node["value"])[0],
                )
            )
            continue

        if node["type"] == "name":
            out.append(
                ast.Name(id=node["name"], ctx=ctx_klass()),
            )
            continue

        if node["type"] == "expr":
            out.append(
                ast.Expr(
                    value=parse_nodes(node["value"])[0]
                )
            )
            continue

        if node["type"] == "function":
            body_nodes = parse_nodes(node["body"])
            out.append(
                ast.FunctionDef(
                    name=node["name"],
                    args=ast.arguments(
                        args=[
                            ast.arg(
                                arg=x["name"],
                                annotation=None,
                            ) for x in node["args"]
                        ],
                        posonlyargs=[],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        defaults=[]
                    ),
                    body=body_nodes,
                    decorator_list=[],
                )
            )
            continue

        if node["type"] == "if":
            test_nodes = parse_nodes(node["test"])
            body_nodes = parse_nodes(node["body"])
            else_nodes = parse_nodes(node["else"])

            out.append(
                ast.If(
                    test=test_nodes[0],
                    body=body_nodes,
                    orelse=else_nodes,
                )
            )
            continue

        if node["type"] == "for":
            target_expr = parse_nodes(node["target"], ctx_klass=ast.Store)
            body_expr = parse_nodes(node["body"])

            iteration_nodes = node["iteration"]

            # Apply range constructor
            if iteration_nodes[0]["type"] == "tuple":
                iteration_expr = [
                    ast.Call(
                        func=ast.Name(id='get_for_range', ctx=ast.Load()),
                        args=parse_nodes(iteration_nodes[0]["value"]),
                        keywords=[],
                    )
                ]

            else:
                iteration_expr = parse_nodes(iteration_nodes)

            out.append(
                ast.For(
                    target=target_expr[0],
                    iter=iteration_expr[0],
                    body=body_expr,
                    orelse=[]
                )
            )
            continue

        if node["type"] == "while":
            test_nodes = parse_nodes(node["test"])
            body_nodes = parse_nodes(node["body"])

            out.append(
                ast.While(
                    test=test_nodes[0],
                    body=body_nodes,
                    orelse=[],
                )
            )

        if node["type"] == "else":
            body_nodes = parse_nodes(node["body"])
            out = out + body_nodes
            continue

        if node["type"] == "call":
            if node["name"] == "#":
                out.append(
                    ast.Call(
                        func=ast.Name(id='len', ctx=ast.Load()),
                        args=parse_nodes(node["args"]),
                        keywords=[],
                    )
                )
                continue

            if node["name"] == "[":
                value_node = node["args"][0]
                value_expression = parse_nodes([value_node])[0]

                out.append(
                    ast.Subscript(
                        value=value_expression,
                        slice=ast.Index(
                            value=parse_nodes(node["args"][1])[0]
                        ),
                        ctx=ast.Load(),
                    )
                )

                continue

            if node["name"] == "=":
                name_arg = node["args"][0]
                value_arg = node["args"][1]

                target_expr = parse_nodes([name_arg], ctx_klass=ast.Store)
                value_expr = parse_nodes(value_arg)

                out.append(
                    ast.Assign(
                        targets=target_expr,
                        value=value_expr[0],
                    )
                )
                continue

            if node["name"] in ["-", "%", "+", "..", "*", "/"]:
                ops = node["name"]

                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                ops_ref = {
                    "-": ast.Sub,
                    "%": ast.Mod,
                    "+": ast.Add,
                    "..": ast.Add,
                    "*": ast.Mult,
                    "/": ast.Div,
                }

                out.append(
                    ast.BinOp(
                        left=arg_left[0],
                        op=ops_ref[ops](),
                        right=arg_right[0],
                    )
                )
                continue

            if node["name"] in ["and", "or"]:
                ops = node["name"]

                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                ops_ref = {
                    "and": ast.And,
                    "or": ast.Or,
                }

                out.append(
                    ast.BoolOp(
                        op=ops_ref[ops](),
                        values=[
                            arg_left[0],
                            arg_right[0],
                        ]
                    )
                )
                continue

            if node["name"] in [">", "<", "~=", "==", "<=", ">="]:
                ops = node["name"]

                arg_left = parse_nodes([node["args"][0]])
                arg_right = parse_nodes(node["args"][1])

                ops_ref = {
                    ">": ast.Gt,
                    ">=": ast.GtE,
                    "<": ast.Lt,
                    "<=": ast.LtE,
                    "~=": ast.NotEq,
                    "==": ast.Eq,
                }

                out.append(
                    ast.Compare(
                        left=arg_left[0],
                        ops=[ops_ref[ops]()],
                        comparators=arg_right,
                    )
                )
                continue

            if node["name"] == "not":
                out.append(
                    ast.UnaryOp(
                        op=ast.Not(),
                        operand=parse_nodes(node["args"])[0]
                    )
                )
                continue

            out.append(
                ast.Call(
                    func=ast.Name(id=node["name"], ctx=ast.Load()),
                    args=parse_nodes(node["args"], ctx_klass=ast.Load),
                    keywords=[]
                )
            )
            continue

    return out
#### INTERFACE ####

def warn(msg):
    sys.stderr.write("\033[1;33m" + "warning: " + "\033[0m" + msg)
def info(msg):
    sys.stderr.write("\033[1;32m" + "info: " + "\033[0m" + msg)
def error(msg):
    sys.stderr.write("\033[1;31m" + "error: " + "\033[0m" + msg + "\n")
    sys.exit()
    
def usage():
    print("\n"+f"""usage: \033[1;33mrbxpy\033[0m [file] [options] > [gen]
\033[1mOptions:\033[0m
{TAB}\033[1m-v\033[0m        show version information
{TAB}\033[1m-vd\033[0m       show version number only"
{TAB}\033[1m-ast\033[0m      show python ast tree before code
{TAB}\033[1m-s\033[0m        generate std.lua
{TAB}\033[1m-u\033[0m        open this""")
    sys.exit()

def version():
    print("\033[1;34m" + "copyright:" + "\033[0m" + " roblox-py " + "\033[1m" + VERSION + "\033[0m" + " licensed under the GNU Affero General Public License by " + "\033[1m" + "@AsynchronousAI" + "\033[0m")
    sys.exit(0)

"""The main entry point to the translator"""
def main():
    """Entry point function to the translator"""
    args = sys.argv[1:]
    ast = False
    input_filename = "NONE"
    type = 1 # 1: py->lua, 2: lua->py
    for arg in args:
        if arg == "-v":
            version()
        elif arg == "-vd":
            print(VERSION)
            sys.exit()
        elif arg == "-u":
            usage()
        elif arg == "-s":
            error("In development")
        elif arg == "-ast":
            ast = True
        elif arg == "-py":
            type = 1
        elif arg == "-lua":
            type = 2
        else:
            input_filename = arg
            
    if type == 1:
        if input_filename == "NONE":
            usage()
        if not Path(input_filename).is_file():
            error(
                "The given filename ('{}') is not a file.".format(input_filename))

        content = None
        with open(input_filename, "r") as file:
            content = file.read()

        if not content:
            error("The input file is empty.")

        translator = Translator(Config(".pyluaconf.yaml"),
                                show_ast=ast)
        lua_code = translator.translate(content)

        if not ast:
            print(lua_code)
    else:
        file_handler = open(input_filename, 'r')
        source = file_handler.read()

        tokens = lexer(source)

        #if kwargs["strip_comments"]:
        #    tokens = list(filter(lambda x: x["type"] != "COMMENT", tokens))
        #    tokens = list(filter(lambda x: x["type"] != "MULTILINE-COMMENT", tokens))

        #if kwargs["tokens"]:
        #    pprint(tokens)
        #    return

        ast_ = parse(tokens)

        #if kwargs["ast"]:
        #    pprint(ast_)
        #    return

        py_ast = ast_to_py_ast(ast_)

        #if kwargs["py_ast"]:
        #    print(ast.dump(py_ast))
        #    return

        #if kwargs["py_code"]:
        #    print(astunparse.unparse(py_ast))
        #    return

        print(PY_HEADER + astunparse.unparse(py_ast))
    return 0


if __name__ == "__main__":
    sys.exit(main())