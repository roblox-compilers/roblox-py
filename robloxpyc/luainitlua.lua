--// AsynchronousAI @Dev98799 \\--
----------------------------------------------------------------------------------------
-- stdlib used to hold built in functions wrappers and libraries                      --
----------------------------------------------------------------------------------------

-- stdlib Version 2.5.9 --

local module = { }

-- Language used for gamewrapper (from Highlighter by boatbomber)
local language = {
	builtin = {
		-- Luau Functions
		["assert"] = "function",
		["error"] = "function",
		["getfenv"] = "function",
		["getmetatable"] = "function",
		["ipairs"] = "function",
		["loadstring"] = "function",
		["newproxy"] = "function",
		["next"] = "function",
		["pairs"] = "function",
		["pcall"] = "function",
		["print"] = "function",
		["rawequal"] = "function",
		["rawget"] = "function",
		["rawlen"] = "function",
		["rawset"] = "function",
		["select"] = "function",
		["setfenv"] = "function",
		["setmetatable"] = "function",
		["tonumber"] = "function",
		["tostring"] = "function",
		["unpack"] = "function",
		["xpcall"] = "function",

		-- Luau Functions (Deprecated)
		["collectgarbage"] = "function",

		-- Luau Variables
		["_G"] = "table",
		["_VERSION"] = "string",

		-- Luau Tables
		["bit32"] = "table",
		["coroutine"] = "table",
		["debug"] = "table",
		["math"] = "table",
		["os"] = "table",
		["string"] = "table",
		["table"] = "table",
		["utf8"] = "table",

		-- Roblox Functions
		["DebuggerManager"] = "function",
		["delay"] = "function",
		["gcinfo"] = "function",
		["PluginManager"] = "function",
		["require"] = "function",
		["settings"] = "function",
		["spawn"] = "function",
		["tick"] = "function",
		["time"] = "function",
		["UserSettings"] = "function",
		["wait"] = "function",
		["warn"] = "function",

		-- Roblox Functions (Deprecated)
		["Delay"] = "function",
		["ElapsedTime"] = "function",
		["elapsedTime"] = "function",
		["printidentity"] = "function",
		["Spawn"] = "function",
		["Stats"] = "function",
		["stats"] = "function",
		["Version"] = "function",
		["version"] = "function",
		["Wait"] = "function",
		["ypcall"] = "function",

		-- Roblox Variables
		["game"] = "Instance",
		["plugin"] = "Instance",
		["script"] = "Instance",
		["shared"] = "Instance",
		["workspace"] = "Instance",

		-- Roblox Variables (Deprecated)
		["Game"] = "Instance",
		["Workspace"] = "Instance",

		-- Roblox Tables
		["Axes"] = "table",
		["BrickColor"] = "table",
		["CatalogSearchParams"] = "table",
		["CFrame"] = "table",
		["Color3"] = "table",
		["ColorSequence"] = "table",
		["ColorSequenceKeypoint"] = "table",
		["DateTime"] = "table",
		["DockWidgetPluginGuiInfo"] = "table",
		["Enum"] = "table",
		["Faces"] = "table",
		["FloatCurveKey"] = "table",
		["Font"] = "table",
		["Instance"] = "table",
		["NumberRange"] = "table",
		["NumberSequence"] = "table",
		["NumberSequenceKeypoint"] = "table",
		["OverlapParams"] = "table",
		["PathWaypoint"] = "table",
		["PhysicalProperties"] = "table",
		["Random"] = "table",
		["Ray"] = "table",
		["RaycastParams"] = "table",
		["Rect"] = "table",
		["Region3"] = "table",
		["Region3int16"] = "table",
		["RotationCurveKey"] = "table",
		["SharedTable"] = "table",
		["task"] = "table",
		["TweenInfo"] = "table",
		["UDim"] = "table",
		["UDim2"] = "table",
		["Vector2"] = "table",
		["Vector2int16"] = "table",
		["Vector3"] = "table",
		["Vector3int16"] = "table",
	},

	libraries = {

		-- Luau Libraries
		bit32 = {
			arshift = "function",
			band = "function",
			bnot = "function",
			bor = "function",
			btest = "function",
			bxor = "function",
			countlz = "function",
			countrz = "function",
			extract = "function",
			lrotate = "function",
			lshift = "function",
			replace = "function",
			rrotate = "function",
			rshift = "function",
		},

		coroutine = {
			close = "function",
			create = "function",
			isyieldable = "function",
			resume = "function",
			running = "function",
			status = "function",
			wrap = "function",
			yield = "function",
		},

		debug = {
			dumpheap = "function",
			getmemorycategory = "function",
			info = "function",
			loadmodule = "function",
			profilebegin = "function",
			profileend = "function",
			resetmemorycategory = "function",
			setmemorycategory = "function",
			traceback = "function",
		},

		math = {
			abs = "function",
			acos = "function",
			asin = "function",
			atan2 = "function",
			atan = "function",
			ceil = "function",
			clamp = "function",
			cos = "function",
			cosh = "function",
			deg = "function",
			exp = "function",
			floor = "function",
			fmod = "function",
			frexp = "function",
			ldexp = "function",
			log10 = "function",
			log = "function",
			max = "function",
			min = "function",
			modf = "function",
			noise = "function",
			pow = "function",
			rad = "function",
			random = "function",
			randomseed = "function",
			round = "function",
			sign = "function",
			sin = "function",
			sinh = "function",
			sqrt = "function",
			tan = "function",
			tanh = "function",

			huge = "number",
			pi = "number",
		},

		os = {
			clock = "function",
			date = "function",
			difftime = "function",
			time = "function",
		},

		string = {
			byte = "function",
			char = "function",
			find = "function",
			format = "function",
			gmatch = "function",
			gsub = "function",
			len = "function",
			lower = "function",
			match = "function",
			pack = "function",
			packsize = "function",
			rep = "function",
			reverse = "function",
			split = "function",
			sub = "function",
			unpack = "function",
			upper = "function",
		},

		table = {
			clear = "function",
			clone = "function",
			concat = "function",
			create = "function",
			find = "function",
			foreach = "function",
			foreachi = "function",
			freeze = "function",
			getn = "function",
			insert = "function",
			isfrozen = "function",
			maxn = "function",
			move = "function",
			pack = "function",
			remove = "function",
			sort = "function",
			unpack = "function",
		},

		utf8 = {
			char = "function",
			codepoint = "function",
			codes = "function",
			graphemes = "function",
			len = "function",
			nfcnormalize = "function",
			nfdnormalize = "function",
			offset = "function",

			charpattern = "string",
		},

		-- Roblox Libraries
		Axes = {
			new = "function",
		},

		BrickColor = {
			Black = "function",
			Blue = "function",
			DarkGray = "function",
			Gray = "function",
			Green = "function",
			new = "function",
			New = "function",
			palette = "function",
			Random = "function",
			random = "function",
			Red = "function",
			White = "function",
			Yellow = "function",
		},

		CatalogSearchParams = {
			new = "function",
		},

		CFrame = {
			Angles = "function",
			fromAxisAngle = "function",
			fromEulerAngles = "function",
			fromEulerAnglesXYZ = "function",
			fromEulerAnglesYXZ = "function",
			fromMatrix = "function",
			fromOrientation = "function",
			lookAt = "function",
			new = "function",

			identity = "CFrame",
		},

		Color3 = {
			fromHex = "function",
			fromHSV = "function",
			fromRGB = "function",
			new = "function",
			toHSV = "function",
		},

		ColorSequence = {
			new = "function",
		},

		ColorSequenceKeypoint = {
			new = "function",
		},

		DateTime = {
			fromIsoDate = "function",
			fromLocalTime = "function",
			fromUniversalTime = "function",
			fromUnixTimestamp = "function",
			fromUnixTimestampMillis = "function",
			now = "function",
		},

		DockWidgetPluginGuiInfo = {
			new = "function",
		},

		Enum = {},

		Faces = {
			new = "function",
		},

		FloatCurveKey = {
			new = "function",
		},

		Font = {
			fromEnum = "function",
			fromId = "function",
			fromName = "function",
			new = "function",
		},

		Instance = {
			new = "function",
		},

		NumberRange = {
			new = "function",
		},

		NumberSequence = {
			new = "function",
		},

		NumberSequenceKeypoint = {
			new = "function",
		},

		OverlapParams = {
			new = "function",
		},

		PathWaypoint = {
			new = "function",
		},

		PhysicalProperties = {
			new = "function",
		},

		Random = {
			new = "function",
		},

		Ray = {
			new = "function",
		},

		RaycastParams = {
			new = "function",
		},

		Rect = {
			new = "function",
		},

		Region3 = {
			new = "function",
		},

		Region3int16 = {
			new = "function",
		},

		RotationCurveKey = {
			new = "function",
		},

		SharedTable = {
			clear = "function",
			clone = "function",
			cloneAndFreeze = "function",
			increment = "function",
			isFrozen = "function",
			new = "function",
			size = "function",
			update = "function",
		},

		task = {
			cancel = "function",
			defer = "function",
			delay = "function",
			desynchronize = "function",
			spawn = "function",
			synchronize = "function",
			wait = "function",
		},

		TweenInfo = {
			new = "function",
		},

		UDim = {
			new = "function",
		},

		UDim2 = {
			fromOffset = "function",
			fromScale = "function",
			new = "function",
		},

		Vector2 = {
			new = "function",

			one = "Vector2",
			xAxis = "Vector2",
			yAxis = "Vector2",
			zero = "Vector2",
		},

		Vector2int16 = {
			new = "function",
		},

		Vector3 = {
			fromAxis = "function",
			FromAxis = "function",
			fromNormalId = "function",
			FromNormalId = "function",
			new = "function",

			one = "Vector3",
			xAxis = "Vector3",
			yAxis = "Vector3",
			zAxis = "Vector3",
			zero = "Vector3",
		},

		Vector3int16 = {
			new = "function",
		},
	},
}

-- Filling up language.libraries.Enum table
local enumLibraryTable = language.libraries.Enum

for _, enum in ipairs(Enum:GetEnums()) do
	--TODO: Remove tostring from here once there is a better way to get the name of an Enum
	enumLibraryTable[tostring(enum)] = "Enum"
end

local function parse_path(path, start_obj)
	local obj = start_obj or game
	local parts = string.split(path, "/")
	for i, part in ipairs(parts) do
		if part == "" then
			obj = game
		elseif part == "~" then
			obj = game
		elseif part == ".." then
			obj = obj.Parent
		else
			obj = obj:FindFirstChild(part)
			if not obj then
				error("Object not found: " .. part)
			end
		end
	end
	return obj
end


local slicefun = function (seq, start, stop, step)
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

local function set_metatable(var, mt)
	local var_type = typeof(var)
	if var_type == "Instance" then
		var:SetAttribute("__metatable", mt)
	elseif var_type == "table" or var_type == "userdata" then
		setmetatable(var, mt)
	elseif var_type == "number" or var_type == "string" or var_type == "boolean" then
		local proxy = newproxy(true)
		getmetatable(proxy).__index = function() return var end
		setmetatable(proxy, mt)
		var = proxy
	end
	return var
end
local function set_fun_meta(f, rmt)
	return function()
		local returnval = f()
		if returnval == nil then return end
		if type(returnval) == "function" then
			return set_fun_meta(returnval, rmt)
		else
			set_metatable(rmt)
		end
	end
end
local gtype 
if not typeof then
	gtype = function(obj)
		local type = type(obj)
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


function string_meta(input)
	if type(input) == "string" then
		return set_metatable(input, {
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
						if (not stop) and (not step) and start then -- 1 value
							start = string.match(index, "SLICE!%((%d+), (%d+)%)")
							step = 1
							stop = -1
						elseif not step then
							start, stop = string.match(index, "SLICE!%((%d+), (%d+)%)")
							step = 1
						end
						return slicefun(self, tonumber(start), tonumber(stop), tonumber(step))
					end
				end
				return input:split()[index]
			end,
			__newindex = function(self, index, value)
				input:split()[index] = value
			end,
			__tostring = function(self)
				return input
			end,
			__call = function(self, ...)
				return string.format(input, ...)
			end,
			__sub = function(v1, v2)
				if typeof(v1) == "string" and typeof(v2) == "string" then
					return string.gsub(v1, v2, "")
				end
				return v1 - v2
			end,
			__mul = function(v1, v2)
				if typeof(v1) == "string" then
					return string.rep(v1, v2)
				end
				return v1 * v2
			end,

		})
	else
		return input
	end
end
function list(input)
	if type(input) == "table" then
		setmetatable(input, {
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
								if (not stop) and (not step) and start then -- 1 value
									start = string.match(index, "SLICE!%((%d+), (%d+)%)")
									step = 1
									stop = -1
								elseif not step then
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
		return input
	else
		error("Class mismatch")
		return input
	end
end
function dict(input)
	if type(input) == "table" then
		setmetatable(input, {
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
			end,
		})
		return input
	else
		error("Class mismatch")
		return input
	end
end
local pymeta = function()
	local meta = {}
end


--{SOURCECODEGOESHERE}--

local libraries = {
	["example"] = function() print("Example library!") end,
	--{ITEMSGOHERE}--
}
local dependenciesfolder = script.Parent
local pythonBuiltIn = function(inScript) -- python built in
	return {game = pymeta(game),
		stringmeta = string_meta, list = list, dict = dict, -- class meta
		staticmethod = function(old_fun) -- staticmethod
			local wrapper = function(first, ...)
				return old_fun(...)
			end

			return wrapper
		end,
		classmethod = function(old_fun) -- classmethod
			local wrapper = function(first, ...)
				return old_fun(first, ...)
			end

			return wrapper
		end,
		class = function(class_init, bases) -- class
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
		range = function(s, e) -- range()
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
		__name__ = if inScript:IsA("BaseScript") then "__main__" else inScript.Name , 
		len = function(x) return #x end, -- len()
		abs = math.abs, -- abs()
		str = tostring, -- str()
		int = tonumber, -- int()

		sum = function(tbl) --sum()
			local total = 0
			for _, v in ipairs(tbl) do
				total = total + v
			end
			return total
		end,

		-- Maximum value in a table
		max = function(tbl) --max()
			local maxValue = -math.huge
			for _, v in ipairs(tbl) do
				if v > maxValue then
					maxValue = v
				end
			end
			return maxValue
		end,

		-- Minimum value in a table
		min = function(tbl) --min()
			local minValue = math.huge
			for _, v in ipairs(tbl) do
				if v < minValue then
					minValue = v
				end
			end
			return minValue
		end,

		-- Reversed version of a table or string
		reversed = function(seq) -- reversed()
			local reversedSeq = {}
			local length = #seq
			for i = length, 1, -1 do
				reversedSeq[length - i + 1] = seq[i]
			end
			return reversedSeq
		end,

		-- Splitting a string into a table of substrings
		split = function(str, sep) -- split
			local substrings = {}
			local pattern = string.format("([^%s]+)",sep or "%s")
			for substring in string.gmatch(str, pattern) do
				table.insert(substrings, substring)
			end
			return substrings
		end,

		round = math.round, -- round()

		all = function (iter) -- all()
			for i, v in iter do if not v then return false end end

			return true
		end,

		any = function (iter) -- any()
			for i, v in iter do
				if v then return true end
			end
			return false
		end,

		ord = string.byte, -- ord
		chr = string.char, -- chr

		callable = function(fun) -- callable()
			if rawget(fun) ~= fun then warn("At the momement Roblox.py's function callable() does not fully support metatables.") end
			return typeof(rawget(fun))	== "function"
		end,
		float = tonumber, -- float()
		super = function()
			error("roblox-pyc does not has a Lua implementation of the function `super`. Use `self` instead")
		end,
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
		end,

		hex = function (value) -- hex
			return string.format("%x", value)
		end,

		id = function (obj) -- id
			return print(tostring({obj}):gsub("table: ", ""):split(" ")[1])
		end,
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
		end,
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
		end,
		divmod = function(a, b) -- divmod
			local res = { math.floor(a / b), math.fmod(a, b) }
			return unpack(res)
		end,
		slice = slicefun,	
		operator_in = function (item, items) -- operator_in()
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
		asynchronousfunction = function(func) -- asynchronousfunction
			return function(...)
				local all = {...}
				coroutine.wrap(function()
					func(unpack(all))
				end)()
			end
		end,
		match = function(value, values) -- match
			if values[value] then
				return values[value]()
			elseif values["default"] then
				return values["default"]() 
			end
		end,

		anext = function (iterator) -- anext
			local status, value = pcall(iterator)
			if status then
				return value
			end
		end,

		ascii = function (obj) -- ascii
			return string.format("%q", tostring(obj))
		end,
		dir = function (obj) -- dir
			local result = {}
			for key, _ in pairs(obj) do
				table.insert(result, key)
			end
			return result
		end,
		getattr = function (obj, name, default) -- getattr
			local value = obj[name]
			if value == nil then
				return default
			end
			return value
		end,
		globals = function () -- globals
			return _G
		end,
		hasattr = function (obj, name) --hasattr
			return obj[name] ~= nil
		end,
		input = function (prompt) -- input
			if not io then error("io is not enabled") end
			io.write(prompt)
			return io.read()
		end,
		isinstance = function (obj, class) -- isinstance
			return type(obj) == class
		end,
		issubclass = function (cls, classinfo) -- issubclass
			local mt = getmetatable(cls)
			while mt do
				if mt.__index == classinfo then
					return true
				end
				mt = getmetatable(mt.__index)
			end
			return false
		end,
		iter = function (obj) -- iter
			if type(obj) == "table" and obj.__iter__ ~= nil then
				return obj.__iter__
			end
			return nil
		end,
		locals = function () -- locals
			return _G
		end,
		-- oct()
		oct = function (num) --oct
			return string.format("%o", num)
		end,

		-- open()
		open = function (path, mode)
				local obj = parse_path(path, game)
				if obj:IsA("ModuleScript") then
					local source = obj.Source
					if mode == "r" then
						return source
					elseif mode == "w" then
						return {
							write = function(self, data)
								obj:SetSource(data)
							end,
							close = function(self)
								--obj:SaveSource()
								return -- do nothing
							end
						}
					else
						error("Invalid mode, at the moment only r and w are supported: " .. mode)
					end
				else
					error("Object is not a LuaSourceContainer: " .. path)
				end
		end,


		-- pow()
		pow = function (base, exponent, modulo) --pow
			if modulo ~= nil then
				return math.pow(base, exponent) % modulo
			else
				return base ^ exponent
			end
		end,

		-- eval()
		eval = function (expr, env)
			return loadstring(expr)
		end,

		-- exec()
		exec = loadstring,

		-- filter()
		filter = function (predicate, iterable)
			local result = {}
			for _, value in ipairs(iterable) do
				if predicate(value) then
					table.insert(result, value)
				end
			end
			return result
		end,

		-- frozenset()
		frozenset = function (...)
			local elements = {...}
			local frozenSet = {}
			for _, element in ipairs(elements) do
				frozenSet[element] = true
			end
			return frozenSet
		end,
		-- aiter()
		aiter = function (iterable) -- aiter
			return pairs(iterable)
		end,

		-- bin()
		bin = function(num: number)
			local bits = {}
			repeat
				table.insert(bits, 1, num % 2)
				num = math.floor(num / 2)
			until num == 0
			return "0b" .. table.concat(bits)
		end,
		-- complex() 
		complex = function (real, imag) -- complex
			return { real = real, imag = imag }
		end,

		-- delattr()
		deltaattr = function (object, attribute) -- delattr
			object[attribute] = nil
		end,	

		-- enumerate()
		enumerate = function (iterable) -- enumerate
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
		breakpoint = function () -- breakpoint
			-- This function can be left empty or you can add a debug hook to pause execution.
			-- Here's an example using the debug library to pause execution:

			print("Breakpoint hit, we would reccomend using roblox breakpoints.")
			--io.read() -- Wait for user input to continue

		end,

		-- bytearray()
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
		end,

		-- bytes()
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
		end,

		-- compile()
		compile = loadstring,


		-- help()
		help = function (object) -- help
			-- This is a placeholder implementation and might not cover all possible use cases.
			-- You would need to provide your own implementation based on your specific requirements.
			-- Here's an example of displaying a help message for an object:
			print("Help for object:", object)
			print("Type:", type(object))
			print("Learn more in the official roblox documentation!")
		end,

		-- memoryview()
		memoryview = function (object) -- memoryview
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
		repr = function (object) -- repr
			-- This is a placeholder implementation and might not cover all possible use cases.
			-- You would need to provide your own implementation based on your specific requirements.
			-- Here's an example of generating a representation of an object:
			return tostring(object)
		end,

		-- sorted()
		sorted = function (iterable, cmp, key, reverse) -- sorted
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
		vars = function (object) -- vars
			-- This is a placeholder implementation and might not cover all possible use cases.
			-- You would need to provide your own implementation based on your specific requirements.
			-- Here's an example of getting the attributes of an object:
			local attributes = {}
			for key, value in pairs(object) do
				attributes[key] = value
			end
			return attributes
		end,

		__import__ = require,

		formatmod = function (left, right)
			if type(left) == "string" then
				return string.format(left, right)
			elseif type(left) == "table" then
				local result = {}
				for i, v in ipairs(left) do
					result[i] = string.format(v, right)
				end
				return result
			elseif type(left) == "number" then
				return math.fmod(left, right)
			else
				error("Invalid argument type for %")
			end
		end
	}
end
local import = function(index, sub) -- import
	if libraries[index] then
		if sub then
			return libraries[index][sub]
		else
			return libraries[index]
		end
	elseif script.Parent:FindFirstChildOfClass("ModuleScript") then
		return require(script.Parent:FindFirstChildOfClass("ModuleScript"))
	elseif script.Parent:FindFirstChildOfClass("Folder") then
		if require(script.Parent:FindFirstChildOfClass("Folder"):FindFirstChild("init") or script.Parent:FindFirstChildOfClass("Folder"):FindFirstChild(sub)) then
			return require(script.Parent:FindFirstChildOfClass("Folder"):FindFirstChild("init") or script.Parent:FindFirstChildOfClass("Folder"):FindFirstChild(sub))
		elseif script.Parent:FindFirstChildOfClass("Folder"):FindFirstChild("default.project") and script.Parent:FindFirstAncestorOfClass("Folder"):FindFirstChild("default.project"):IsA("ModuleScript") then
			local jsondata = require(script.Parent:FindFirstAncestorOfClass("Folder"):FindFirstChild("default.project"))
			if jsondata["Type"] and jsondata["Type"] == "json" then
				jsondata = jsondata["Contents"]
			end
		end
	else
		error("No such library called " .. index)
	end
end
local module = function(scriptname)
	return { 
		py = {
			import,
			pythonBuiltIn(scriptname)
		},
		lunar = {
			import,
			{-- lunar built in NOTHING
			},
		},
		c = {
			import,
			{-- c and c++ built in
			}
		}
	}
end



_G.pyc = module
