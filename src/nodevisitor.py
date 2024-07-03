"""Node visitor"""

import ast
from tokenend import TokenEndMode
from context import Context
from log import error, warn
from symbols import *
from binop import *
from boolop import *
from compop import *
from const import *
from loopcounter import *
from luau import *
from symbols import *
from translator import *
from config import *
import lib
from unary import *

# Note from @AsynchronousAI: This file is legit the compiler, if u wanna change up the generated code use this.
dependencies = []
exports = []


class NodeVisitor(ast.NodeVisitor):
    LUACODE = "luau"

    """Node visitor"""

    def __init__(self, context=None, config=None, variables=None, functions=None):
        self.context = context if context is not None else Context()
        self.config = config
        self.last_end_mode = TokenEndMode.LINE_FEED
        self.output = []
        self.variables = variables if variables is not None else {}
        self.functions = functions if functions is not None else []

    def visit_YieldFrom(self, node):
        """Visit yield from"""
        self.emit(
            "for _, v in {} do coroutine.yield(v) end".format(
                self.visit_all(node.value, inline=True)
            )
        )

    def get_variable_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        return None


    def visit_Assign(self, node):
        """Visit assign"""

        for target in node.targets:
            var_name = self.get_variable_name(target)
            if var_name:
                var_value_node = node.value
                if isinstance(var_value_node, ast.Constant):
                    var_type = type(var_value_node.value).__name__
                else:
                    var_type = type(var_value_node).__name__

                self.variables[var_name] = var_type

        target = self.visit_all(node.targets[0], inline=True)
        value = self.visit_all(node.value, inline=True)
        if "," in target:
            t2 = target.replace(" ", "").split(",")
            i = 0
            while i <= (len(t2) - 1):
                if t2[i] in reserves:
                    error(f"'{t2[i]}' is a reserved Luau keyword.")
                else:
                    i += 1

        local_keyword = ""

        last_ctx = self.context.last()

        if last_ctx["class_name"]:
            target = ".".join([last_ctx["class_name"], target])

        if target.isalnum() and not last_ctx["locals"].exists(target):
            local_keyword = "local "
            last_ctx["locals"].add_symbol(target)

        if target in reserves or target in lib.libs:
            error(f"'{target}' is a reserved Luau keyword.")

        self.emit(
            "{local}{target} = {value}".format(
                local=local_keyword, target=target, value=value
            )
        )

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
                self.emit(
                    "{}if {} == {} then".format(
                        first, self.visit_all(node.subject, inline=True), val
                    )
                )
                self.visit_all(case.body)
            else:
                #    self.emit("else")
                #    self.visit_all(case.body)
                error(
                    "Match statement requires a compile-time constant, not a variable."
                )
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
                line = line.format(self.visit_all(i.optional_vars, inline=True))
            line += self.visit_all(i.context_expr, inline=True)
            lines.append(line)
        for line in lines:
            body.insert(0, line)
        self.emit("end)")

    def visit_Slice(self, node):
        if node.lower:
            lower = self.visit_all(node.lower, inline=True)
        else:
            lower = "0"
        lower += ", "
        if node.upper:
            upper = self.visit_all(node.upper, inline=True)
        else:
            upper = "0"
        upper += ", "
        if node.step:
            step = self.visit_all(node.step, inline=True)
        else:
            step = "0"

        self.emit("slice({}{}{})".format(lower, upper, step))

    def visit_JoinedStr(self, node):
        # f"{a} {b}"
        # becomes
        # `{a} {b}`

        """Visit joined string"""
        values = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                values.append(value.s)
            else:
                values.append(self.visit_all(value, inline=True))
        self.emit(repr("`{}`".format("".join(values)))[1:-1])

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
        istype = last_ctx["class_name"] == "TYPE"
        if last_ctx["class_name"] and not istype:
            target = ".".join([last_ctx["class_name"], target])
        if "." not in target and not last_ctx["locals"].exists(target):
            local_keyword = "local "
            last_ctx["locals"].add_symbol(target)
        type = self.visit_all(node.annotation, inline=True)

        if value != None and value != "":
            self.emit(
                "{local}{target} = {value}".format(
                    local=local_keyword, target=target, value=value
                )
            )
        else:
            if istype:
                self.emit("{target},".format(target=target))
            else:
                if node.annotation.__class__.__name__ == "Call":
                    self.visit_Call(node.annotation, target)
                else:
                    self.emit(
                        "{local}{target} = nil".format(
                            local=local_keyword, target=target
                        )
                    )
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
        if (
            (values["object"].startswith('"') and values["object"].endswith('"'))
            or (values["object"].startswith("'") and values["object"].endswith("'"))
            or (values["object"].startswith("{") and values["object"].endswith("}"))
            or (values["object"].startswith("[") and values["object"].endswith("]"))
            or (values["object"].startswith("`") and values["object"].endswith("`"))
        ):
            values["object"] = "({})".format(values["object"])

        self.emit(line.format(**values))

    def visit_BinOp(self, node):
        """Visit binary operation"""
        operation = BinaryOperationDesc.OPERATION[node.op.__class__]

        if operation["depend"]:
            self.depend(operation["depend"])

        line = "({})".format(operation["format"])

        left_value = self.visit_all(node.left, inline=True)
        right_value = self.visit_all(node.right, inline=True)
        left_is_str = (
            isinstance(node.left, ast.Constant)
            and isinstance(node.left.value, str)
            or self.variables.get(left_value) == "str"
        )
        right_is_str = (
            isinstance(node.right, ast.Constant)
            and isinstance(node.right.value, str)
            or self.variables.get(right_value) == "str"
        )
        if operation["value"] == "*":
            if left_is_str or self.variables.get(left_value) == "str":
                line = "string.rep({left},{right})"
            elif right_is_str or self.variables.get(right_value) == "str":
                line = "string.rep({right},{left})"

        if operation["value"] == "+":
            # Checks for list + list
            if self.variables.get(left_value) == "list" or isinstance(
                node.left, ast.List
            ):
                if self.variables.get(right_value) == "list" or isinstance(
                    node.right, ast.List
                ):
                    pass
                else:
                    error("Not supported.")
            if left_is_str and right_is_str:
                line = "{} .. {}".format(left_value, right_value)
                self.emit(line)
                return
            elif left_is_str or right_is_str:
                # Handle the case when one operand is a string and the other is not
                if left_is_str:
                    line = "{} .. tostring({})".format(left_value, right_value)
                else:
                    line = "tostring({}) .. {}".format(left_value, right_value)
                self.emit(line)
                return
            else:
                # Handle the case when neither operand is a string
                values = {
                    "left": left_value,
                    "right": right_value,
                    "operation": operation["value"],
                }
                line = line.format(**values)
                self.emit(line)
                return

        else:
            values = {
                "left": left_value,
                "right": right_value,
                "operation": operation["value"],
            }
            line = line.format(**values)
            self.emit(line)

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

    def visit_Call(self, node, method=None):
        """Visit function call"""

        def parse_expr(d):
            if isinstance(d, ast.Name):
                return d.id
            elif isinstance(d, ast.Attribute):
                return f"{parse_expr(d.value)}.{d.attr}"
            elif isinstance(d, ast.List):  # Handling list literals
                elements = ", ".join([ast.unparse(el) for el in d.elts])
                return "{" + f"{elements}" + "}"
            else:
                return ast.unparse(d)

        line = "{name}({arguments})"

        name = self.visit_all(node.func, inline=True)

        if str(name) == "complex":
            self.depend("complex")
        if method:
            name = method + ":" + name
        arguments = [self.visit_all(arg, inline=True) for arg in node.args]

        if isinstance(node.func, ast.Attribute):
            # Assuming the first argument exists and is what we want to inspect
            match node.func.attr:
                case "append":
                    arg_value = ast.parse(node.args[0])
                    self.emit(
                        "table.insert({},{})".format(
                            parse_expr(node.func.value), parse_expr(arg_value)
                        )
                    )
                    return
                case "reverse":
                    self.emit(
                        "table.sort({},{})".format(
                            parse_expr(node.func.value),
                            "(function(a,b) return a > b end)",
                        )
                    )
                    return
                case "clear":
                    self.emit("table.clear({})".format(parse_expr(node.func.value)))
                    return
                case "pop":
                    arg_value = ast.parse(node.args[0])
                    self.emit(
                        "table.remove({},{})".format(
                            parse_expr(node.func.value), (arg_value.value) + 1
                        )
                    )
                    return
                case "copy":
                    self.emit("table.copy({})".format(parse_expr(node.func.value)))
                    return
                case "insert":
                    arg_value = ast.parse(node.args[0])
                    self.emit(
                        "table.insert({},{},{})".format(
                            parse_expr(node.func.value),
                            int(parse_expr(arg_value)) + 1,
                            parse_expr(ast.parse(node.args[1])),
                        )
                    )
                    return
                case "remove":
                    arg_value = ast.parse(node.args[0])
                    self.emit(
                        "table.remove({},{})".format(
                            parse_expr(node.func.value), parse_expr(arg_value)
                        )
                    )
                    return
                case "sort":
                    kwargs = {}
                    for keyword in node.keywords:
                        kwargs[keyword.arg] = self.visit_all(keyword.value, inline=True)
                    if len(kwargs) == 1 and kwargs.get("reverse", False):
                        self.emit(
                            "table.sort({},{})".format(
                                parse_expr(node.func.value),
                                "(function(a,b) return a > b end)",
                            )
                        )
                        return
                    elif len(kwargs) == 1 and kwargs.get("key", False):
                        error("The key kwarg is not supported.")
                    else:
                        error("The key kwarg is not supported.")

                case "count":
                    arg = node.args[0]

                    self.emit("""
(function(tbl, val)
	local result = 0
	for _,v in tbl do
		if v == val then
			result += 1
		end
	end
	return result
end)({}, {})
""".format(parse_expr(node.func.value),parse_expr(arg)))
                    return

                case "index":
                    args = 0
                    for _ in node.args:
                        args += 1

                    if args == 1:
                       self.emit("table.find({},{})".format(
                           parse_expr(node.func.value),parse_expr(node.args[0])
                       ))
                       return
                    elif args == 2:
                        self.emit("table.find({},{},{})".format(parse_expr(node.func.value),parse_expr(node.args[0]),parse_expr(node.args[1])))
                        return
                    else:
                        self.emit("""
(function(tbl, val, start, stop)
	for index = start, stop do
		if tbl[index] == val then
			return index
		end
	end
	return nil
end)({}, {}, {}, {})""".format(parse_expr(node.func.value),parse_expr(node.args[0]),parse_expr(node.args[1]),parse_expr(node.args[2])))
                    return
                        

                case "extend":
                    arg_value = ast.parse(node.args[0])
                    self.emit(
                        """
for _,i in {} do
    table.insert({},i)

""".format(parse_expr(arg_value), parse_expr(node.func.value))
                    )
                    return

        self.emit(line.format(name=name, arguments=", ".join(arguments)))

    def visit_TypeAlias(self, node):
        if self.config["luau"] == None:
            warn(
                'in your \033[1m.robloxpy.json\033[0m file, specify weather or not to export Luau types like \033[1m"luau": true\033[0m`. Ignoring type alias.'
            )
        elif self.config["luau"] == True:
            self.emit(
                "type {} = {}".format(
                    node.name.id, self.visit_all(node.value, inline=True)
                )
            )

    def visit_ClassDef(self, node):
        """Visit class definition"""
        bases = [self.visit_all(base, inline=True) for base in node.bases]

        # if "type" in bases:
        # self.emit("type {} = {{".format(node.name, self.visit_all(node.bases[0], inline=True)))
        # self.context.push({"class_name": "TYPE"})
        # self.visit_all(node.body)
        # self.context.pop()
        # self.emit("}")
        # else:
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
        for i, (op, comparator) in enumerate(zip(node.ops, node.comparators)):
            operation = CompareOperationDesc.OPERATION.get(op.__class__)
            right = self.visit_all(comparator, inline=True)

            values = {
                "left": left,
                "operation": operation,
                "right": right,
            }
            if op.__class__.__name__ == "In" or op.__class__.__name__ == "NotIn":
                op_str = "not" if op.__class__.__name__ == "NotIn" else ""
                leftval = type(node.left).__name__
                rightval = type(comparator).__name__

                if leftval == 'Constant':
                    leftval = (type(node.left.value).__name__).capitalize()
                if rightval == 'Name':
                    x = self.visit_all(comparator, inline=True)
                    rightval = self.variables.get(x)
                if rightval == 'Constant':
                    rightval = (type(comparator.value).__name__).capitalize()
                if leftval == 'Name':
                    x = self.visit_all(node.left, inline=True)
                    leftval = self.variables.get(x)
                ##IN CHECK##
                if rightval == 'List':
                    line += f"{op_str}(table.find({right},{left}))"
                elif rightval == 'Str':
                    line += f"{op_str}(string.find({right}, {left}, 1, true) ~= nil)"
            else:
                line += f"{values['left']} {values['operation']} {values['right']}"

            if i < len(node.ops) - 1:
                left = right
                line += " and "

        self.emit(line)


    def visit_Continue(self, node):
        """Visit continue"""
        last_ctx = self.context.last()
        line = "continue"
        self.emit(line)

    def visit_Delete(self, node):
        """Visit delete"""
        targets = [self.visit_all(target, inline=True) for target in node.targets]
        nils = ["nil" for _ in targets]
        line = "{targets} = {nils}".format(
            targets=", ".join(targets), nils=", ".join(nils)
        )
        self.emit(line)

    def visit_Dict(self, node):
        """Visit dictionary"""
        keys = []

        for key in node.keys:
            value = self.visit_all(key, inline=True)
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
        if isinstance(node.value, ast.Constant):
            self.functions[-1]["body"].append(node.value.value)
        expr_is_docstring = False
        if isinstance(node.value, ast.Constant):
            expr_is_docstring = True

        self.context.push({"docstring": expr_is_docstring})
        output = self.visit_all(node.value)
        self.context.pop()

        self.output.append(output)

    def visit_FunctionDef(self, node):
        """Visit function definition"""
        line = "{local} function {name}({arguments})"

        self.functions.append(
            {
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "returns": None,
                "body": [],
            }
        )

        last_ctx = self.context.last()

        name = node.name
        type = 1  # 1 = static, 2 = class
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

        function_def = line.format(
            local=local_keyword, name=name, arguments=", ".join(arguments)
        )

        self.emit(function_def)

        self.context.push({"class_name": ""})
        self.visit_all(node.body)
        self.context.pop()

        body = self.output[-1]

        if node.args.vararg is not None:
            line = "local {name} = {{...}}".format(name=node.args.vararg.arg)
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

        # exports.append(name)

    def visit_For(self, node):
        """Visit for loop"""
        values = {
            "target": self.visit_all(node.target, inline=True),
            "iter": self.visit_all(node.iter, inline=True),
        }

        line = "for {target} in {iter} do"

        if isinstance(node.iter, ast.Constant):
            line = 'for {target} in string.gmatch({iter},".") do'

        if values["iter"] in self.variables:
            if self.variables[values["iter"]] == "str":
                line = 'for {target} in string.gmatch({iter},".") do'
            else:
                line = "for {target} in {iter} do"
        self.emit(line.format(**values))

        continue_label = LoopCounter.get_next()
        self.context.push(
            {
                "loop_label_name": continue_label,
            }
        )
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
        type = 1  # 1 = static, 2 = class
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

        function_def = line.format(
            local=local_keyword, name=name, arguments=", ".join(arguments)
        )

        self.emit(function_def)

        self.context.push({"class_name": ""})
        self.visit_all(node.body)
        self.context.pop()

        body = self.output[-1]

        if node.args.vararg is not None:
            line = f"local {node.args.vararg.arg} = {...}"
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

        # exports.append(name)

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
                _elseif = node.orelse[0]
                elseif_test = self.visit_all(_elseif.test, inline=True)

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

    def visit_Import(self, node, og=True):
        """Visit import"""
        line = 'local {asname} = rcc.import("{name}", script) or require("{name}")'
        values = {"asname": "", "name": ""}

        if og:
            for v in node.names:
                self.visit_Import(v, False)
            return

        if node.name.startswith("game."):
            line = 'local {asname} = game:GetService("{name}")'
            values["name"] = node.name[5:]

        if node.asname is None:
            if not node.name.startswith("game."):
                values["name"] = node.name
            values["asname"] = values["name"]
            values["asname"] = values["asname"].split(".")[-1]
        else:
            values["asname"] = node.asname
            if not node.name.startswith("game."):
                values["name"] = node.name

        if node.name in lib.libs:
            self.emit(getattr(libs, node.name))
            return

        self.emit(line.format(**values))

    def visit_ImportFrom(self, node):
        """Visit import from"""
        module = node.module
        if module is None:
            module = ""
        else:
            module = module

        if module == "services" or module == "rbx.services":
            for name in node.names:
                if name.asname is None:
                    if name.name == "*":
                        error("import * is unsupproted")
                    else:
                        self.emit(
                            'local {name} = game:GetService("{name}")'.format(
                                name=name.name,
                            )
                        )
                else:
                    if name.name == "*":
                        error("import * is unsupproted")
                    else:
                        self.emit(
                            'local {name} = game:GetService("{realname}")'.format(
                                name=name.asname,
                                realname=name.name,
                            )
                        )
        elif module == "rbx":
            for name in node.names:
                if name.asname is None:
                    if name.name == "*":
                        continue
                    else:
                        self.emit(
                            'local {name} = game:GetService("{name}")'.format(
                                name=name.name,
                            )
                        )
                else:
                    if name.name == "*":
                        continue
                    else:
                        self.emit(
                            'local {name} = game:GetService("{realname}")'.format(
                                name=name.asname,
                                realname=name.name,
                            )
                        )
        else:
            for name in node.names:
                if name.asname is None:
                    if name.name == "*":
                        error("import * is unsupproted")
                    else:
                        self.emit(
                            'local {name} = (rcc.import("{module}") or require("{module}")).{name}'.format(
                                name=name.name,
                                module=module,
                            )
                        )
                else:
                    if name.name == "*":
                        error("import * is unsupproted")
                    else:
                        self.emit(
                            'local {name} = (rcc.import("{module}") or require("{module}")).{realname}'.format(
                                name=name.asname,
                                module=module,
                                realname=name.name,
                            )
                        )

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
        line = "{{{}}}".format(", ".join(elements))
        self.emit(line)

    def visit_GeneratorExp(self, node):
        """Visit generator expression"""
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

        line = "result.append({})"
        line = line.format(self.visit_all(node.elt, inline=True))
        self.emit(line)

        self.emit(" ".join(["end"] * ends_count))

        self.emit("return result")
        self.emit("end)()")

    def visit_ListComp(self, node):
        """Visit list comprehension"""
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

        line = (
            "table.insert(result._data,"
            + "{"
            + str(self.visit_all(node.elt, inline=True))
            + "}"
        )
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
        self.emit(str(node.value))

    def visit_Pass(self, node):
        """Visit pass"""
        pass

    def visit_Return(self, node):
        """Visit return"""
        line = "return "
        if node.value:
            self.functions[-1]["returns"] = (
                str(self.visit_all(node.value, inline=True)).strip("(").strip(")")
            )
        line += self.visit_all(node.value, inline=True)
        self.emit(line)

    def visit_Starred(self, node):
        """Visit starred object"""
        value = self.visit_all(node.value, inline=True)
        line = "unpack({})".format(value)
        self.emit(line)

    def visit_Str(self, node):
        """Visit str"""
        value = repr(node.s)
        if value.startswith(NodeVisitor.LUACODE):
            value = value[len(NodeVisitor.LUACODE) :]
            self.emit(value)
        elif self.context.last()["docstring"]:
            self.emit("--[[ {} ]]".format(node.s))
        else:
            self.emit(repr("{}".format(node.s)))

    def visit_Subscript(self, node):
        """Visit subscript"""
        line = "{name}{indexs}"
        index = self.visit_all(node.slice, inline=True)
        indexs = []
        final = ""

        # Split index by toplevel , and add each index to indexs
        # This is done to support multiple indexes
        # Example: a[1, 2, 3] -> a[1][2][3]
        # but a[x(1,2), b(3, 4)] -> a[x(1,2)][b(3, 4)]

        depth = 0
        for char in index:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "," and depth == 0:
                indexs.append(index[: index.find(char)])
                index = index[index.find(char) + 1 :]
        indexs.append(index)

        # Generate final
        for i in indexs:
            final += "[{}]".format(i)

        values = {
            "name": self.visit_all(node.value, inline=True),
            "indexs": final,
        }
        if values["name"] in reserves:
            error(f"'{values['name']}'is a reserved Luau keyword.")

        self.emit(line.format(**values))

    def visit_Tuple(self, node):
        """Visit tuple"""
        elements = [self.visit_all(item, inline=True) for item in node.elts]
        line = "table.freeze({{{}}})".format(", ".join(elements))
        self.emit(line)

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
        self.emit("{" + ", ".join(values) + "}")

    def visit_Try(self, node):
        """Visit try"""
        self.emit("--> try statement start:")
        self.emit("xpcall(function()")

        self.visit_all(node.body)

        self.emit("end, function(err)")
        ifD = False
        for i, handler in enumerate(node.handlers):
            self.emit("--> try: {}".format(i))
            if ((handler.type) != None) and hasattr(handler.type, "id"):
                if i == 0:
                    ifD = True
                    an = "if"
                else:
                    an = "elseif"
                if (
                    handler.type.id != "Exception"
                    or handler.type.id != "BaseException"
                    or handler.type.id != "Error"
                ):
                    self.emit(f"{an} err:find('{handler.type.id}') then")
                else:
                    self.emit(f"{an} err then")

                if handler.name != None:
                    self.emit(f"\tlocal {handler.name} = err")
            self.visit_all(handler.body)
            if (i == len(node.handlers) - 1) and ifD:
                self.emit("end")

        self.emit("end)")
        self.visit_all(node.finalbody)

        self.emit("--> try statement end")

    def visit_While(self, node):
        """Visit while"""
        test = self.visit_all(node.test, inline=True)

        self.emit("while {} do".format(test))

        continue_label = LoopCounter.get_next()
        self.context.push(
            {
                "loop_label_name": continue_label,
            }
        )
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
                line = line.format(self.visit_all(i.optional_vars, inline=True))
            line += self.visit_all(i.context_expr, inline=True)
            lines.append(line)

        for line in lines:
            body.insert(0, line)

        self.emit("end")

    def visit_all(self, nodes, inline=False):
        """Visit all nodes in the given list"""

        if not inline:
            last_ctx = self.context.last()
            last_ctx["locals"].push()

        visitor = NodeVisitor(
            context=self.context,
            config=self.config,
            variables=self.variables,
            functions=self.functions,
        )

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

    def get_dependencies(self):
        return dependencies

    def get_exports(self):
        return exports
