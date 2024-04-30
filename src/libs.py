# This file includes Lua snippets

json = """local json = {}
function json.loads(t)
    return game.HttpService:JSONEncode(t)
end
function json.dumps(t)
    return game.HttpService:JSONDecode(t)
end
function fault()
    error("[roblox-py] (json-lib) Outputting to files is not supported.")
end
json.load, json.dump = fault, fault"""

# libs = ["json"]

TYPS = """""" # old
errs = ["ValueError", "TypeError", "AttributeError", "IndexError", "KeyError", "ZeroDivisionError", "AssertionError", "NotImplementedError", "RuntimeError", "NameError", "SyntaxError", "IndentationError", "TabError", "ImportError", "ModuleNotFoundError", "OSError", "FileNotFoundError", "PermissionError", "EOFError", "ConnectionError", "TimeoutError", "UnboundLocalError", "RecursionError", "MemoryError", "OverflowError", "FloatingPointError", "ArithmeticError", "ReferenceError", "SystemError", "SystemExit", "GeneratorExit", "KeyboardInterrupt", "StopIteration", "Exception", "BaseException", "Error"]
libs = ["class", "op_is", "dict", "list", "op_in", "safeadd", "safeloop", "__name__", "range", "len", "abs", "str", "int", "sum", "max", "min", "reversed", "split", "round", "all", "any", "ord", "chr", "callable", "float", "super", "format", "hex", "id", "map", "bool", "divmod", "slice", "anext", "ascii", "dir", "getattr", "globals", "hasattr", "isinstance", "issubclass", "iter", "locals", "oct", "pow", "eval", "exec", "filter", "frozenset", "aiter", "bin", "complex", "deltaattr", "enumerate", "bytearray", "bytes", "compile", "help", "memoryview", "repr", "sorted", "vars", "tuple"]

DEPENDENCY = """\n\n--> imports
py = _G.rbxpy or require(game.ReplicatedStorage.Packages.pyruntime)
if game.ReplicatedStorage:FindFirstChild("Packages") and game.ReplicatedStorage.Packages:FindFirstChild("rcclib") then
    rcc = _G.rcc or require(game.ReplicatedStorage.Packages.rcclib)
else
    rcc = { }
    setmetatable(rcc, {__index = function(_, index) return function()end end})
end
"""
IS = """\n\nfunction op_is(a, b)
        warn("[roblox-py] is serves no purpose when compiling to Lua, use == instead")
        return a == b
    end"""
ADD = """\n\nfunction safeadd(a, b)
        if type(a) == "string" or type(b) == "string" then
            return a .. b
        elseif type(a) == "table" and type(b) == "table" then
            local result = {}
            for _, v in ipairs(a) do
                table.insert(result, v)
            end
            for _, v in ipairs(b) do
                table.insert(result, v)
            end
            return result
        else
            return a + b
        end
    end"""
FN = """\n\nif game then
    __name__ = (if script:IsA("BaseScript") then "__main__" else script.Name)
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

    enumerate = function (t)
	local i = 0
	return function()
		i = i + 1
		local value = t(nil, i)
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
IN =  """\n\nfunction op_in(item, items)
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
CLASS = """\n\nfunction class(class_init, bases)
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
DICT =  """\n\nfunction dict(t)
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
LIST = """\n\nfunction list(t,check)
	local result = {}

	if check == false then
		result.is_list = false
	else
		result._is_list = true
	end

	result._data = {}
	for _, v in ipairs(t) do
		table.insert(result._data, v)
	end

	if check == false then
		table.freeze(result._data)
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
		__len = function(self)
			return #self._data
		end
	})

	return result
end"""

TUPLE = """\n\nfunction tuple(t)
	return list(t,false)
end"""