#!/usr/bin/env python3
import sys, ast, yaml, re, os, subprocess
from pprint import pprint
from pathlib import Path
from enum import Enum

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
            "format": "op_in({left}, {right})",
            "depend": "in",
        },
        ast.NotIn: {
            "format": "not op_in({left}, {right})",
            "depend": "in",
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
exports = []

class NodeVisitor(ast.NodeVisitor):
    LUACODE = "luau"

    """Node visitor"""
    def __init__(self, context=None, config=None):
        self.context = context if context is not None else Context()
        self.config = config
        self.last_end_mode = TokenEndMode.LINE_FEED
        self.output = []

    def visit_YieldFrom(self, node):
        """Visit yield from"""
        self.emit("for _, v in {} do coroutine.yield(v) end".format(self.visit_all(node.value, inline=True)))
        
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
        
        #exports.append(target)

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
                
                val = case.pattern.value.s
                if isinstance(val, str):
                    val = '"{}"'.format(val)
                self.emit("{}if {} == {} then".format(first, self.visit_all(node.subject, inline=True), val))
                self.visit_all(case.body)
            else:
            #    self.emit("else")
            #    self.visit_all(case.body)
                error("Match statement requires a compile-time constant, not a variable.")
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
        self.emit("task.spawn(function()")
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
        self.emit("end)")
        
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
        self.emit("[[{}]]".format(node.s.decode("utf8")))
        
        
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
        istype = (last_ctx["class_name"] == "TYPE")
        if last_ctx["class_name"] and not istype:
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
        else:
            if istype:
                self.emit("{target}: {type},".format(local=local_keyword,
                                                            target=target,
                                                            type=type))
            else:
                if node.annotation.__class__.__name__ == "Call":
                    self.visit_Call(node.annotation, target)
                else:
                    self.emit("{local}{target} = nil".format(local=local_keyword,
                                                            target=target,
                                                            type=type))
        # example input:
        # a: int = 1
        # example output:
        # local a = 1
        
    def visit_AugAssign(self, node):
        """Visit augassign"""
        operation = BinaryOperationDesc.OPERATION[node.op.__class__]
        
        if operation["depend"]:
            self.depend(operation["depend"])

        target = self.visit_all(node.target, inline=True)

        values = {
            "left": target,
            "right": self.visit_all(node.value, inline=True),
            "operation": operation["value"],
        }

        line = "({})".format(operation["format"])
        #if operation["depend"]:
        #    self.depend(operation["depend"])
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
        
        if operation["depend"]:
            self.depend(operation["depend"])
            
        line = "({})".format(operation["format"])
        #if operation["depend"]: Binary operators do not have it
        #    self.depend(operation["depend"])
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
        #if operation["depend"]:
        #    self.depend(operation["depend"])
        values = {
            "left": self.visit_all(node.values[0], True),
            "right": self.visit_all(node.values[1], True),
            "operation": operation["value"],
        }

        self.emit(line.format(**values))

    def visit_Break(self, node):
        """Visit break"""
        self.emit("break")

    def visit_Call(self, node, method = None):
        """Visit function call"""
        line = "{name}({arguments})"

        name = self.visit_all(node.func, inline=True)
        if method:
            name = method + ":" + name
        arguments = [self.visit_all(arg, inline=True) for arg in node.args]

        self.emit(line.format(name=name, arguments=", ".join(arguments)))

    def visit_ClassDef(self, node):
        """Visit class definition"""
        bases = [self.visit_all(base, inline=True) for base in node.bases]
        
        if "type" in bases:
            self.emit("type {} = {{".format(node.name, self.visit_all(node.bases[0], inline=True)))
            self.context.push({"class_name": "TYPE"})
            self.visit_all(node.body)
            self.context.pop()
            self.emit("}")
        else:
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
                if operation["depend"]:
                    self.depend(operation["depend"])

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
        self.depend("dict")
            
    def visit_DictComp(self, node):
        """Visit dictionary comprehension"""
        self.emit("(function()")
        self.depend("dict")
        self.emit("local result = dict {}")
        self.depend("dict")

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
            line = "{name} = {decorator}:Connect({name})".format(**values)
            self.emit(line)
        
        #exports.append(name)

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
            exports.append(name)

    def visit_AsyncFunctionDef(self, node):
        """Visit async function definition"""
        line = "{local}function {name}({arguments}) task.spawn(function()"

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

        self.emit("end) end")

        for decorator in reversed(node.decorator_list):
            decorator_name = self.visit_all(decorator, inline=True)
            if decorator_name == "classmethod" or decorator_name == "staticmethod":
                continue
            values = {
                "name": name,
                "decorator": decorator_name,
            }
            line = "{name} = {decorator}:Connect({name})".format(**values)
            self.emit(line)
        
        #exports.append(name)
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

        if node.names[0].name.startswith("game."):
            line = 'local {asname} = game:GetService("{name}")'
            values["name"] = node.names[0].name[5:]
            
        if node.names[0].asname is None:
            if not node.names[0].name.startswith("game."):
                values["name"] = node.names[0].name
            values["asname"] = values["name"]
            values["asname"] = values["asname"].split(".")[-1]
        else:
            values["asname"] = node.names[0].asname
            if not node.names[0].name.startswith("game."):
                values["name"] = node.names[0].name

        self.emit(line.format(**values))
    
    def visit_ImportFrom(self, node):
        """Visit import from"""
        module = node.module
        if module is None:
            module = ""
        else:
            module = module

        if module == "services":
            for name in node.names:
                if name.asname is None:
                    if name.name == "*":
                        error("import * is unsupproted")
                    else:
                        self.emit("local {name} = game:GetService(\"{name}\")".format(
                            name=name.name,
                            module=module,
                        ))
                else:
                    if name.name == "*":
                        error("import * is unsupproted")
                    else:
                        self.emit("local {name} = game:GetService(\"{realname}\")".format(
                            name=name.asname,
                            module=module,
                            realname=name.name,
                        ))
        else:
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
        self.depend("list")
        self.emit(line)

    def visit_GeneratorExp(self, node):
        """Visit generator expression"""
        self.emit("(function()")
        self.emit("local result = list {}")
        self.depend("list")
    
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
                
    def visit_ListComp(self, node):
        """Visit list comprehension"""
        self.emit("(function()")
        self.emit("local result = list {}")
        self.depend("list")

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
        #if operation["depend"]:
        #    self.depend(operation["depend"])
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
        if (node.type) != None:
            if not hasattr(node.type, "id"):
                error("'except' type had an invalid value (expected 'name')")
                sys.exit(1)
            if node.type.id != "Exception" or node.type.id != "BaseException" or node.type.id != "Error":
                self.emit("if err:find('{}') then".format(node.type.id))
            else:
                self.emit("if err then")
                
            if node.name != None:
                self.emit("\tlocal {} = err".format(node.name)) # The \n does messup the token generator, but makes cleaner code
        
        self.visit_all(node.body)
        
        if (node.type) != None:
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
      if value != "":
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

    def translate(self, pycode, fn, isAPI = False, export = True, reqfile = False, useRequire = False):
        """Translate python code to lua code"""
        DEPEND = "\n\n--// REQUIREMENTS \\\\--\n"
        
        if not reqfile:
            if isAPI: 
                py_ast_tree = ast.parse(pycode)
            else:
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
            
            self.output = visitor.output
            
            # Remove duplicates from dependencies (list)
            global dependencies
            dependencies = list(set(dependencies))
            
            global exports
            exports = list(set(exports))
            
            if fn:
                dependencies.append("fn")
            if export and exports != []:
                FOOTER = "\n\n--// EXPORTS \\\\--\n"
                FOOTER += "if not script:IsA(\"BaseScript\") then\n\treturn {\n"
                for export in exports:
                    FOOTER += f"\t\t[\"{export}\"] = {export},\n"
                FOOTER += "\t}\nend"
            else:
                FOOTER = ""
            
        if reqfile:
            dependencies = ["class", "dict", "list", "in", "fn", "safeadd"]
        if not useRequire:
            for depend in dependencies:
                # set
                
                if depend == "list":
                    DEPEND += """\n\nfunction list(t)
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
                    DEPEND += """\n\nfunction dict(t)
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

                local key_index, value = next(result._data, key_index)
                return value
            end
        end

        setmetatable(result, {
            __index = function(self, index)
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
                    DEPEND += """\n\nfunction class(class_init, bases)
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

     	    meta = {
	  	__add = object.__add__,
    		__sub = object.__sub__,
      		__div = object.__div__,
		__unm = object.__unm,
	   }


            return setmetatable(object, meta)
        end

        setmetatable(c, mt)

        return c
    end"""      
                elif depend == "in":
                    DEPEND += """\n\nfunction op_in(item, items)
        if type(items) == "table" then
            for v in items do
                if v == item then
                    return true
                end
            end
        elseif type(items) == "string" and type(item) == "string" then
            return string.find(items, item, 1, true) ~= nil
        end

        return false
    end"""
                elif depend == "fn":
                    DEPEND += """\n\nif game then
    __name__ = if script:IsA("BaseScript") then "__main__" else script.Name 
    else
    __name__ = nil
    end
    range = function(s, e, f) -- range()
        local tb = {}
        local a = 0
        local b = 0
        local c = 0
        if not e then a=1 else a=s end
        if not e then b=s else b=e end
        if not f then c=1 else c=f end
        for i = a, b, c do
            tb[#tb+1] = i
        end
        return tb
    end
    len = function(x) return #x end -- len()
    abs = math.abs -- abs()
    str = tostring -- str()
    int = tonumber -- int()
    sum = function(tbl) --sum()
        local total = 0
        for _, v in ipairs(tbl) do
            total = total + v
        end
        return total
    end
    max = function(tbl) --max()
        local maxValue = -math.huge
        for _, v in ipairs(tbl) do
            if v > maxValue then
                maxValue = v
            end
        end
        return maxValue
    end
    min = function(tbl) --min()
        local minValue = math.huge
        for _, v in ipairs(tbl) do
            if v < minValue then
                minValue = v
            end
        end
        return minValue
    end
    reversed = function(seq) -- reversed()
        local reversedSeq = {}
        local length = #seq
        for i = length, 1, -1 do
            reversedSeq[length - i + 1] = seq[i]
        end
        return reversedSeq
    end
    split = function(str, sep) -- split
        local substrings = {}
        local pattern = string.format("([^%s]+)",sep or "%s")
        for substring in string.gmatch(str, pattern) do
            table.insert(substrings, substring)
        end
        return substrings
    end
    round = math.round -- round()
    all = function (iter) -- all()
        for i, v in iter do if not v then return false end end

        return true
    end
    any = function (iter) -- any()
        for i, v in iter do
            if v then return true end
        end
        return false
    end
    ord = string.byte -- ord
    chr = string.char -- chr
    callable = function(fun) -- callable()
        if rawget(fun) ~= fun then warn("At the momement Roblox.py's function callable() does not fully support metatables.") end
        return typeof(rawget(fun))	== "function"
    end
    float = tonumber -- float()
    super = function()
        error("roblox-pyc does not has a Lua implementation of the function `super`. Use `self` instead")
    end
    format = function(format, ...) -- format
        local args = {...}
        local num_args = select("#", ...)

        local formatted_string = string.gsub(format, "{(%d+)}", function(index)
            index = tonumber(index)
            if index >= 1 and index <= num_args then
                return tostring(args[index])
            else
                return "{" .. index .. "}"
            end
        end)

        return formatted_string
    end
    hex = function (value) -- hex
        return string.format("%x", value)
    end
    id = function (obj) -- id
        return print(tostring({obj}):gsub("table: ", ""):split(" ")[1])
    end
    map = function (func, ...) --map
        local args = {...}
        local result = {}
        local num_args = select("#", ...)

        local shortest_length = math.huge
        for i = 1, num_args do
            local arg = args[i]
            local arg_length = #arg
            if arg_length < shortest_length then
                shortest_length = arg_length
            end
        end

        for i = 1, shortest_length do
            local mapped_args = {}
            for j = 1, num_args do
                local arg = args[j]
                table.insert(mapped_args, arg[i])
            end
            table.insert(result, func(unpack(mapped_args)))
        end

        return result
    end
    bool = function(x) -- bool
        if x == false or x == nil or x == 0 then
            return false
        end

        if typeof(x) == "table" then
            if x._is_list or x._is_dict then
                return next(x._data) ~= nil
            end
        end

        return true
    end
    divmod = function(a, b) -- divmod
        local res = { math.floor(a / b), math.fmod(a, b) }
        return unpack(res)
    end
    slice = function (seq, start, stop, step)
        local sliced = {}
        local len = #seq
        start = start or 1
        stop = stop or len
        step = step or 1
        if start < 0 then
            start = len + start + 1
        end
        if stop < 0 then
            stop = len + stop + 1
        end
        for i = start, stop - 1, step do
            table.insert(sliced, seq[i])
        end
        return sliced
    end
    anext = function (iterator) -- anext
        local status, value = pcall(iterator)
        if status then
            return value
        end
    end
    ascii = function (obj) -- ascii
        return string.format("%q", tostring(obj))
    end
    dir = function (obj) -- dir
        local result = {}
        for key, _ in pairs(obj) do
            table.insert(result, key)
        end
        return result
    end
    getattr = function (obj, name, default) -- getattr
        local value = obj[name]
        if value == nil then
            return default
        end
        return value
    end
    globals = function () -- globals
        return _G
    end
    hasattr = function (obj, name) --hasattr
        return obj[name] ~= nil
    end
    isinstance = function (obj, class) -- isinstance
        return type(obj) == class
    end
    issubclass = function (cls, classinfo) -- issubclass
        local mt = getmetatable(cls)
        while mt do
            if mt.__index == classinfo then
                return true
            end
            mt = getmetatable(mt.__index)
        end
        return false
    end
    iter = function (obj) -- iter
        if type(obj) == "table" and obj.__iter__ ~= nil then
            return obj.__iter__
        end
        return nil
    end
    locals = function () -- locals
        return _G
    end
    oct = function (num) --oct
        return string.format("%o", num)
    end
    pow = function (base, exponent, modulo) --pow
        if modulo ~= nil then
            return math.pow(base, exponent) % modulo
        else
            return base ^ exponent
        end
    end
    eval = function (expr, env)
        return loadstring(expr)()
    end
    exec = loadstring
    filter = function (predicate, iterable)
        local result = {}
        for _, value in ipairs(iterable) do
            if predicate(value) then
                table.insert(result, value)
            end
        end
        return result
    end
    frozenset = function (...)
        local elements = {...}
        local frozenSet = {}
        for _, element in ipairs(elements) do
            frozenSet[element] = true
        end
        return frozenSet
    end
    aiter = function (iterable) -- aiter
        return pairs(iterable)
    end
    bin = function(num: number)
        local bits = {}
        repeat
            table.insert(bits, 1, num % 2)
            num = math.floor(num / 2)
        until num == 0
        return "0b" .. table.concat(bits)
    end
    complex = function (real, imag) -- complex
        return { real = real, imag = imag }
    end
    deltaattr = function (object, attribute) -- delattr
        object[attribute] = nil
    end
    enumerate = function (iterable) -- enumerate
        local i = 0
        return function()
            i = i + 1
            local value = iterable[i]
            if value ~= nil then
                return i, value
            end
        end
    end
    bytearray = function (arg) -- bytearray
        if type(arg) == "string" then
            local bytes = {}
            for i = 1, #arg do
                table.insert(bytes, string.byte(arg, i))
            end
            return bytes
        elseif type(arg) == "number" then
            local bytes = {}
            while arg > 0 do
                table.insert(bytes, 1, arg % 256)
                arg = math.floor(arg / 256)
            end
            return bytes
        elseif type(arg) == "table" then
            return arg -- Assuming it's already a bytearray table
        else
            error("Invalid argument type for bytearray()")
        end
    end
    bytes = function (arg) -- bytes
        if type(arg) == "string" then
            local bytes = {}
            for i = 1, #arg do
                table.insert(bytes, string.byte(arg, i))
            end
            return bytes
        elseif type(arg) == "table" then
            return arg -- Assuming it's already a bytes table
        else
            error("Invalid argument type for bytes()")
        end
    end
    compile = loadstring
    help = function (object) -- help
        print("Help for object:", object)
        print("Type:", type(object))
        print("Learn more in the official roblox documentation!")
    end
    memoryview = function (object) -- memoryview
        if type(object) == "table" then
            local buffer = table.concat(object)
            return { buffer = buffer, itemsize = 1 }
        else
            error("Invalid argument type for memoryview()")
        end
    end
    repr = function (object) -- repr
        return tostring(object)
    end
    sorted = function (iterable, cmp, key, reverse) -- sorted
        local sortedTable = {}
        for key, value in pairs(iterable) do
            table.insert(sortedTable, { key = key, value = value })
        end
        table.sort(sortedTable, function(a, b)
            -- Compare logic based on cmp, key, reverse parameters
            return a.key < b.key
        end)
        local i = 0
        return function()
            i = i + 1
            local entry = sortedTable[i]
            if entry then
                return entry.key, entry.value
            end
        end
    end
    vars = function (object) -- vars
        local attributes = {}
        for key, value in pairs(object) do
            attributes[key] = value
        end
        return attributes
    end"""
                elif depend == "safeadd":
                    DEPEND += """\n\nfunction safeadd(a, b)
        if type(a) == "number" and type(b) == "number" then
            return a + b
        elseif type(a) == "string" and type(b) == "string" then
            return a .. b
        else
            error(`Attempt to add a {type(a)} and a {type(b)}`)
        end
    end"""
                else:
                    error("Auto-generated dependency unhandled '{}', please report this issue on Discord or Github".format(depend))
    
        if not reqfile:           
            DEPEND += "\n\n----- CODE START -----\n"  
        else:
            DEPEND += "\n\nreturn env"
            return DEPEND
        
        CODE = self.to_code()
        libs = ["class", "dict", "list", "op_in", "safeadd", "__name__", "range", "len", "abs", "str", "int", "sum", "max", "min", "reversed", "split", "round", "all", "any", "ord", "chr", "callable", "float", "super", "format", "hex", "id", "map", "bool", "divmod", "slice", "anext", "ascii", "dir", "getattr", "globals", "hasattr", "isinstance", "issubclass", "iter", "locals", "oct", "pow", "eval", "exec", "filter", "frozenset", "aiter", "bin", "complex", "deltaattr", "enumerate", "bytearray", "bytes", "compile", "help", "memoryview", "repr", "sorted", "vars"]
        
        if useRequire:
            DEPEND = """\n\n--// Imports \\\\--
py = _G.rbxpy or require(game.ReplicatedStorage.Packages.pyruntime)

"""
            for i in libs:
                if i in CODE:
                    DEPEND += f"{i} = py.{i}"
                    
            DEPEND += "\n\n----- CODE START -----\n"
            

        return HEADER + DEPEND + CODE + FOOTER

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

#class PyGenerator:
    
#### INTERFACE ####
def error(msg):
    print("\033[91;1merror\033[0m \033[90mPY roblox-py:\033[0m " + msg)
def warn(msg):
    sys.stderr.write("\033[1;33m" + "warning: " + "\033[0m" + "\033[90mPY roblox-py:\033[0m " + msg)
def info(msg):
    sys.stderr.write("\033[1;32m" + "info: " + "\033[0m" + "\033[90mPY roblox-py:\033[0m " + msg)
    
    
def usage():
    print("\n"+f"""usage: \033[1;33mrbxpy\033[0m [file] [options] -o [gen]
\033[1mOptions:\033[0m
{TAB}\033[1m-v\033[0m        show version information
{TAB}\033[1m-vd\033[0m       show version number only
{TAB}\033[1m-ast\033[0m      show python ast tree before code
{TAB}\033[1m-f\033[0m        include standard python functions in generated code
{TAB}\033[1m-fn\033[0m       do not include standard python functions in generated code
{TAB}\033[1m-u\033[0m        open this""")
    sys.exit()

def version():
    print("\033[1;34m" + "copyright:" + "\033[0m" + " roblox-py " + "\033[1m" + VERSION + "\033[0m" + " licensed under the GNU Affero General Public License by " + "\033[1m" + "@AsynchronousAI" + "\033[0m")
    sys.exit(0)

def provideerr(err):
    global proverr
    proverr = err
    
"""The main entry point to the translator"""
def main():
    """Entry point function to the translator"""

    args = sys.argv[1:]
    ast = False
    input_filename = "NONE"
    out = "NONE"
    type = 1 # 1: py->lua, 2: lua->py
    includeSTD = False
    export = True
    skip = False
    reqfile = None
    useRequire = False
    
    for arg in args:
        if skip:
            skip = False
            continue
        
        if arg == "-v":
            version()
        elif arg == "-vd":
            print(VERSION)
            sys.exit()
        elif arg == "-u":
            usage()
        elif arg == "-f":
            includeSTD = True
        elif arg == "-s":
            reqfile = True
        elif arg == "-r":
            useRequire = True
        elif arg == "-fn":
            includeSTD = False
        elif arg == "-ne":
            export = False
        elif arg == "-ast":
            ast = True
        elif arg == "-py":
            type = 1
        elif arg == "-o":
            out = args[args.index(arg)+1]
            skip = True
        elif arg == "-lua":
            type = 2
        elif arg == "-clrtxt":
            # Enable support for ANSI escape sequences
            if os.name == "nt":
                os.system("cmd /c \"setx ENABLE_VIRTUAL_TERMINAL_PROCESSING 1\"")
            sys.exit(0)
        else:
            if input_filename != "NONE":
                error("Unexpected argument: '{}'".format(arg))
            input_filename = arg
            
    if type == 1:
        if (input_filename == "NONE") and not reqfile:
            usage()
        if (not Path(input_filename).is_file()) and not reqfile:
            error(
                "The given filename ('{}') is not a file.".format(input_filename))

        if not reqfile:
            content = None
            with open(input_filename, "r") as file:
                content = file.read()

            if not content:
                error("The input file is empty.")

        translator = Translator(Config(".pyluaconf.yaml"),
                                show_ast=ast)
        if reqfile:
            reqcode = translator.translate("", True, False, False, True)
            if out != "NONE":
                with open(out, "w") as file:
                    file.write(reqcode)
            else:
                print(reqcode)
            sys.exit(0)
        else:
            lua_code = translator.translate(content, includeSTD, False, export, False, useRequire)
        
        if not ast:
            if out != "NONE":
                with open(out, "w") as file:
                    file.write(lua_code)
            else:
                print(lua_code)
    else:
        command = "luac -l "+input_filename
        
        try:
            res = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            sys.exit(1)
            
        res = (res.decode("utf-8"))
        
        # Parse
        commands = {}
        
        lines = res.split("\n")
        lines.pop(0)
        lines.pop(0)
        lines.pop(0)
        for line in lines:
            data = line.split("\t")
            if len(data) < 4:
                continue
            num, cmd, args = data[1], data[3], data[4]
            if len(data) > 5:
                data = data[5]
            else:
                data = "NONE"
                
            commands[num] = {"cmd": cmd, "args": args, "data": data}
        res = "\n".join(lines)
        
        print(commands)
        
        # If luac.out is found then remove it
        if Path("luac.out").is_file():
            os.remove("luac.out")
            
    return 0


if __name__ == "__main__":
    sys.exit(main())
