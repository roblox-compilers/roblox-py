initcode = """

								--// AsynchronousAI @Dev98799 \\--
				-------------------------------------------------------------------------------
				-- this script was added by roblox-pyc plugin to give you the full experience.-- 
				-- below you will find lua equivelents of built in python functions, it is   --         
				-- free to use for your personal needs and feel free to edit it, if needed to--
				-- reset it or update it simply delete it and use the plugin again to do so  --
				-------------------------------------------------------------------------------

									-- Version 1.0.0 --

local module = {}
local string_meta = {}
local slicefun = function (sequence, start, stop, step) -- slice
	local sliced = {}
	local len = #sequence

	-- Set default values for start, stop, and step
	start = start or 1
	stop = stop or len
	step = step or 1

	-- Handle negative indices
	if start < 0 then
		start = len + start + 1
	end
	if stop < 0 then
		stop = len + stop + 1
	end

	-- Adjust start and stop values if they are out of bounds
	if start < 1 then
		start = 1
	elseif start > len then
		start = len + 1
	end
	if stop < 1 then
		stop = 1
	elseif stop > len then
		stop = len + 1
	end

	-- Build the sliced table
	for i = start, stop - 1, step do
		table.insert(sliced, sequence[i])
	end

	-- Return the sliced table as a string if the input was a string
	if typeof(sequence) == "string" then
		return table.concat(sliced)
	end

	return sliced
end

local gtype 
if not typeof then
	gtype = function(obj)
		local type = typeof(obj)
		if type == "table" then
			if obj._is_list then
				return "list"
			end
			if obj._is_dict then
				return "dict"
			end
		end
		return type
	end
else 
	gtype = typeof
end
local typeof = gtype



setmetatable(string_meta, {
	__add = function(v1, v2)
		if typeof(v1) == "string" and typeof(v2) == "string" then
			return v1 .. v2
		end
		return v1 + v2
	end,
	__index = function(self, index)
		if typeof(index) == "string" then
			-- if it start with SLICE! then it is a slice, get the start, stop, and step values. sometimes the 3rd value is not there, so we need to check for that
			if string.sub(index, 1, 6) == "SLICE!" then
				local start, stop, step = string.match(index, "SLICE!%((%d+), (%d+), (%d+)%)")
				if not step then
					start, stop = string.match(index, "SLICE!%((%d+), (%d+)%)")
					step = 1
				end
				return slicefun(self, tonumber(start), tonumber(stop), tonumber(step))
			end
		end
	end,

})
local list = {}
setmetatable(list, {
	__call = function(_, t)
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
				if typeof(index) == "string" then
					-- If it starts with SLICE! then it is a slice, get the start, stop, and step values. Sometimes the 3rd value is not there, so we need to check for that
					if string.sub(index, 1, 6) == "SLICE!" then
						local start, stop, step = string.match(index, "SLICE!%((%d+), (%d+), (%d+)%)")
						if not step then
							start, stop = string.match(index, "SLICE!%((%d+), (%d+)%)")
							step = 1
						end
						return slicefun(self, tonumber(start), tonumber(stop), tonumber(step))
					end
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
	end,
})

local dict = {}
setmetatable(dict, {
	__call = function(_, t)
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
						if not step then
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
	end,
})


local module = function(self)
	return {
		string_meta, list, dict, -- class meta
		
		function(old_fun) -- staticmethod
			local wrapper = function(first, ...)
				return old_fun(...)
			end

			return wrapper
		end,
		function(old_fun) -- classmethod
			local wrapper = function(first, ...)
				return old_fun(first, ...)
			end

			return wrapper
		end,
		function(class_init, bases) -- class
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
		end,
		function(s, e) -- range()
			local tb = {}
			local a = 0
			local b = 0
			if not e then a=1 else a=s end
			if not e then b=s else b=e end
			for i = a, b do
				tb[#tb+1] = i
			end
			return tb
		end,
		self.Name:sub(1,#self.Name-3), -- __name__ 
		function(x) return #x end, -- len()
		math.abs, -- abs()
		tostring, -- str()
		tonumber, -- int()

		function(tbl) --sum()
			local total = 0
			for _, v in ipairs(tbl) do
				total = total + v
			end
			return total
		end,

		-- Maximum value in a table
		function(tbl) --max()
			local maxValue = -math.huge
			for _, v in ipairs(tbl) do
				if v > maxValue then
					maxValue = v
				end
			end
			return maxValue
		end,

		-- Minimum value in a table
		function(tbl) --min()
			local minValue = math.huge
			for _, v in ipairs(tbl) do
				if v < minValue then
					minValue = v
				end
			end
			return minValue
		end,

		-- Reversed version of a table or string
		function(seq) -- reversed()
			local reversedSeq = {}
			local length = #seq
			for i = length, 1, -1 do
				reversedSeq[length - i + 1] = seq[i]
			end
			return reversedSeq
		end,

		-- Splitting a string into a table of substrings
		function(str, sep) -- split
			local substrings = {}
			local pattern = string.format("([^%s]+)",sep or "%s")
			for substring in string.gmatch(str, pattern) do
				table.insert(substrings, substring)
			end
			return substrings
		end,

		math.round, -- round()

		function (iter) -- all()
			for i, v in iter do if not v then return false end end

			return true
		end,

		function (iter) -- any()
			for i, v in iter do
				if v then return true end
			end
			return false
		end,

		string.byte, -- ord
		string.char, -- chr

		function(fun) -- callable()
			if rawget(fun) ~= fun then warn("At the momement Roblox.py's function callable() does not fully support metatables.") end
			return typeof(rawget(fun))	== "function"
		end,

		tonumber,
		
		function(format, ...) -- format
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
		end,
		
		function (value) -- hex
			return string.format("%x", value)
		end,
		
		function (obj) -- id
			return print(tostring({obj}):gsub("table: ", ""):split(" ")[1])
		end,
		function (func, ...) --map
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
		end,
		function(x) -- bool
			if x == false or x == nil or x == 0 then
				return false
			end
		
			if typeof(x) == "table" then
				if x._is_list or x._is_dict then
					return next(x._data) ~= nil
				end
			end
		
			return true
		end,
		function(a, b) -- divmod
			local res = { math.floor(a / b), math.fmod(a, b) }
			return unpack(res)
		end,
		slicefun,	
		function (item, items) -- operator_in()
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
		end,
		function(func) -- asynchronousfunction
			return function(...)
				local all = {...}
				coroutine.wrap(function()
					func(unpack(all))
				end)()
			end
		end,
		function(value, values) -- match
			if values[value] then
				return values[value]()
			elseif values["default"] then
				return values["default"]() 
			end
		end,
		
		function (iterator) -- anext
			local status, value = pcall(iterator)
			if status then
				return value
			end
		end,

		function (obj) -- ascii
			return string.format("%q", tostring(obj))
		end,
		function (obj) -- dir
			local result = {}
			for key, _ in pairs(obj) do
				table.insert(result, key)
			end
			return result
		end,
		function (obj, name, default) -- getattr
			local value = obj[name]
			if value == nil then
				return default
			end
			return value
		end,
		function () -- globals
			return _G
		end,
		function (obj, name) --hasattr
			return obj[name] ~= nil
		end,
		function (prompt) -- input
			if not io then error("io is not enabled") end
			io.write(prompt)
			return io.read()
		end,
		function (obj, class) -- isinstance
			return type(obj) == class
		end,
		function (cls, classinfo) -- issubclass
			local mt = getmetatable(cls)
			while mt do
				if mt.__index == classinfo then
					return true
				end
				mt = getmetatable(mt.__index)
			end
			return false
		end,
		function (obj) -- iter
			if type(obj) == "table" and obj.__iter__ ~= nil then
				return obj.__iter__
			end
			return nil
		end,
		function () -- locals
			return _G
		end,
		-- oct()
		function (num) --oct
			return string.format("%o", num)
		end,

		-- open()
		function (filename, mode) --open
			if not io then error("io is not enabled") end
			return io.open(filename, mode)
		end,

		-- ord()
		function (c) --ord
			return string.byte(c)
		end,

		-- pow()
		function (base, exponent, modulo) --pow
			if modulo ~= nil then
				return math.pow(base, exponent) % modulo
			else
				return base ^ exponent
			end
		end,

		-- eval()
		function (expr, env)
			return loadstring(expr)()
		end,

		-- exec()
		function (code, env)
			return loadstring(expr)()
		end,

		-- filter()
		function (predicate, iterable)
			local result = {}
			for _, value in ipairs(iterable) do
				if predicate(value) then
					table.insert(result, value)
				end
			end
			return result
		end,

		-- frozenset()
		function (...)
			local elements = {...}
			local frozenSet = {}
			for _, element in ipairs(elements) do
				frozenSet[element] = true
			end
			return frozenSet
		end,
		-- aiter()
		function (iterable) -- aiter
			return pairs(iterable)
		end,
		
		-- bin()
		function (number) -- bin
			return string.format("%b", number)
		end,
		-- complex() 
		function (real, imag) -- complex
			return { real = real, imag = imag }
		end,
		
		-- delattr()
		function (object, attribute) -- delattr
			object[attribute] = nil
		end,	

		-- enumerate()
		function (iterable) -- enumerate
			local i = 0
			return function()
			i = i + 1
			local value = iterable[i]
			if value ~= nil then
				return i, value
			end
			end
		end,

		-- breakpoint()
		function () -- breakpoint
			-- This function can be left empty or you can add a debug hook to pause execution.
			-- Here's an example using the debug library to pause execution:
			debug.sethook(function()
			io.write("Breakpoint hit! Press Enter to continue...")
			io.read() -- Wait for user input to continue
			end, "c")
		end,
		
		-- bytearray()
		function (arg) -- bytearray
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
		end,
		
		-- bytes()
		function (arg) -- bytes
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
		end,
		
		-- compile()
		function (source, filename, mode) -- compile
			-- This is a placeholder implementation and might not cover all possible use cases.
			-- You would need to provide your own implementation based on your specific requirements.
			-- Here's an example of a simple compilation to execute Lua code directly:
			local compiledFunction = loadstring(source, filename)
			return compiledFunction
		end,

		
		-- help()
		function (object) -- help
			-- This is a placeholder implementation and might not cover all possible use cases.
			-- You would need to provide your own implementation based on your specific requirements.
			-- Here's an example of displaying a help message for an object:
			print("Help for object:", object)
			print("Type:", type(object))
			-- Add more information or documentation here
		end,
		
		-- memoryview()
		function (object) -- memoryview
			-- This is a placeholder implementation and might not cover all possible use cases.
			-- You would need to provide your own implementation based on your specific requirements.
			-- Here's an example of creating a memory view object:
			if type(object) == "table" then
			local buffer = table.concat(object)
			return { buffer = buffer, itemsize = 1 }
			else
			error("Invalid argument type for memoryview()")
			end
		end,
		-- repr()
		function (object) -- repr
			-- This is a placeholder implementation and might not cover all possible use cases.
			-- You would need to provide your own implementation based on your specific requirements.
			-- Here's an example of generating a representation of an object:
			return tostring(object)
		end,
		
		-- sorted()
		function (iterable, cmp, key, reverse) -- sorted
			-- This is a placeholder implementation and might not cover all possible use cases.
			-- You would need to provide your own implementation based on your specific requirements.
			-- Here's an example of sorting an iterable table:
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
		end,
		
		-- vars()
		function (object) -- vars
			-- This is a placeholder implementation and might not cover all possible use cases.
			-- You would need to provide your own implementation based on your specific requirements.
			-- Here's an example of getting the attributes of an object:
			local attributes = {}
			for key, value in pairs(object) do
			attributes[key] = value
			end
			return attributes
		end,
		
		require,
		
		([[object
		type
		int
		float
		complex
		bool
		str
		bytes
		bytearray
		memoryview
		list
		tuple
		range
		set
		frozenset
		dict
		slice
		property
		bool
		ellipsis
		NotImplemented
		super
		file
		IOError
		OSError
		EnvironmentError
		EOFError
		ImportError
		IndexError
		KeyError
		StopIteration
		GeneratorExit
		KeyboardInterrupt
		SystemExit
		Exception
		BaseException
		ArithmeticError
		AssertionError
		AttributeError
		BufferError
		EOFError
		ImportError
		LookupError
		MemoryError
		NameError
		OSError
		OverflowError
		ReferenceError
		RuntimeError
		SyntaxError
		IndentationError
		TabError
		SystemError
		TypeError
		ValueError
		UnicodeError
		UnicodeDecodeError
		UnicodeEncodeError
		UnicodeTranslateError
		Warning
		UserWarning
		DeprecationWarning
		PendingDeprecationWarning
		SyntaxWarning
		RuntimeWarning
		FutureWarning
		ImportWarning
		UnicodeWarning
		BytesWarning
		ResourceWarning
		Generator
		AsyncGenerator
		Iterator
		Coroutine
		AsyncIterator
		ContextManager
		AsyncContextManager
		CallableIterator
		CallableGenerator
		Reversible
		Sized
		Container
		Collection
		MutableSequence
		Sequence
		MutableSet
		Set
		MutableMapping
		Mapping
		MutableSequence
		ByteString
		MutableByteString
		SupportsAbs
		SupportsFloat
		SupportsInt
		SupportsRound
		SupportsComplex
		SupportsBytes
		SupportsComplex
		SupportsBytes
		SupportsComplex
		SupportsRound
		CoroutineWrapperType
		ContextManagerWrapperType
		AbstractEventLoop
		GeneratorWrapperType
		AsyncGeneratorWrapperType
		AsyncContextManagerWrapperType]]):split("\t"),

		{ -- PY library, built in
			services = game,
		}
	}
end



return module
"""