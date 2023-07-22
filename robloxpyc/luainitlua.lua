					--// AsynchronousAI @Dev98799 \\--
----------------------------------------------------------------------------------------
-- This was added by roblox-pyc it includes the typechecker, builtins, import,        --
-- modules, packages finder, and more. It is default to place this      			  --
-- with the name of "roblox.pyc" in ReplicatedStorage. 							      --
----------------------------------------------------------------------------------------

-- Version 1.5.9 --

local module = { }

-- t: a runtime typechecker for Roblox by osyrisrblx

local t = {}

function t.type(typeName)
	return function(value)
		local valueType = type(value)
		if valueType == typeName then
			return true
		else
			return false, string.format("%s expected, got %s", typeName, valueType)
		end
	end
end

function t.typeof(typeName)
	return function(value)
		local valueType = typeof(value)
		if valueType == typeName then
			return true
		else
			return false, string.format("%s expected, got %s", typeName, valueType)
		end
	end
end

--[[**
	matches any type except nil

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
function t.any(value)
	if value ~= nil then
		return true
	else
		return false, "any expected, got nil"
	end
end

--Lua primitives

--[[**
	ensures Lua primitive boolean type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.boolean = t.typeof("boolean")

--[[**
	ensures Lua primitive thread type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.thread = t.typeof("thread")

--[[**
	ensures Lua primitive callback type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.callback = t.typeof("function")
t["function"] = t.callback

--[[**
	ensures Lua primitive none type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.none = t.typeof("nil")
t["nil"] = t.none

--[[**
	ensures Lua primitive string type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.string = t.typeof("string")

--[[**
	ensures Lua primitive table type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.table = t.typeof("table")

--[[**
	ensures Lua primitive userdata type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.userdata = t.type("userdata")

--[[**
	ensures value is a number and non-NaN

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
function t.number(value)
	local valueType = typeof(value)
	if valueType == "number" then
		if value == value then
			return true
		else
			return false, "unexpected NaN value"
		end
	else
		return false, string.format("number expected, got %s", valueType)
	end
end

--[[**
	ensures value is NaN

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
function t.nan(value)
	local valueType = typeof(value)
	if valueType == "number" then
		if value ~= value then
			return true
		else
			return false, "unexpected non-NaN value"
		end
	else
		return false, string.format("number expected, got %s", valueType)
	end
end

-- roblox types

--[[**
	ensures Roblox Axes type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Axes = t.typeof("Axes")

--[[**
	ensures Roblox BrickColor type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.BrickColor = t.typeof("BrickColor")

--[[**
	ensures Roblox CatalogSearchParams type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.CatalogSearchParams = t.typeof("CatalogSearchParams")

--[[**
	ensures Roblox CFrame type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.CFrame = t.typeof("CFrame")

--[[**
	ensures Roblox Color3 type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Color3 = t.typeof("Color3")

--[[**
	ensures Roblox ColorSequence type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.ColorSequence = t.typeof("ColorSequence")

--[[**
	ensures Roblox ColorSequenceKeypoint type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.ColorSequenceKeypoint = t.typeof("ColorSequenceKeypoint")

--[[**
	ensures Roblox DateTime type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.DateTime = t.typeof("DateTime")

--[[**
	ensures Roblox DockWidgetPluginGuiInfo type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.DockWidgetPluginGuiInfo = t.typeof("DockWidgetPluginGuiInfo")

--[[**
	ensures Roblox Enum type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Enum = t.typeof("Enum")

--[[**
	ensures Roblox EnumItem type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.EnumItem = t.typeof("EnumItem")

--[[**
	ensures Roblox Enums type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Enums = t.typeof("Enums")

--[[**
	ensures Roblox Faces type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Faces = t.typeof("Faces")

--[[**
	ensures Roblox FloatCurveKey type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.FloatCurveKey = t.typeof("FloatCurveKey")

--[[**
	ensures Roblox Font type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Font = t.typeof("Font")

--[[**
	ensures Roblox Instance type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Instance = t.typeof("Instance")

--[[**
	ensures Roblox NumberRange type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.NumberRange = t.typeof("NumberRange")

--[[**
	ensures Roblox NumberSequence type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.NumberSequence = t.typeof("NumberSequence")

--[[**
	ensures Roblox NumberSequenceKeypoint type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.NumberSequenceKeypoint = t.typeof("NumberSequenceKeypoint")

--[[**
	ensures Roblox OverlapParams type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.OverlapParams = t.typeof("OverlapParams")

--[[**
	ensures Roblox PathWaypoint type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.PathWaypoint = t.typeof("PathWaypoint")

--[[**
	ensures Roblox PhysicalProperties type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.PhysicalProperties = t.typeof("PhysicalProperties")

--[[**
	ensures Roblox Random type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Random = t.typeof("Random")

--[[**
	ensures Roblox Ray type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Ray = t.typeof("Ray")

--[[**
	ensures Roblox RaycastParams type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.RaycastParams = t.typeof("RaycastParams")

--[[**
	ensures Roblox RaycastResult type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.RaycastResult = t.typeof("RaycastResult")

--[[**
	ensures Roblox RBXScriptConnection type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.RBXScriptConnection = t.typeof("RBXScriptConnection")

--[[**
	ensures Roblox RBXScriptSignal type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.RBXScriptSignal = t.typeof("RBXScriptSignal")

--[[**
	ensures Roblox Rect type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Rect = t.typeof("Rect")

--[[**
	ensures Roblox Region3 type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Region3 = t.typeof("Region3")

--[[**
	ensures Roblox Region3int16 type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Region3int16 = t.typeof("Region3int16")

--[[**
	ensures Roblox TweenInfo type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.TweenInfo = t.typeof("TweenInfo")

--[[**
	ensures Roblox UDim type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.UDim = t.typeof("UDim")

--[[**
	ensures Roblox UDim2 type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.UDim2 = t.typeof("UDim2")

--[[**
	ensures Roblox Vector2 type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Vector2 = t.typeof("Vector2")

--[[**
	ensures Roblox Vector2int16 type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Vector2int16 = t.typeof("Vector2int16")

--[[**
	ensures Roblox Vector3 type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Vector3 = t.typeof("Vector3")

--[[**
	ensures Roblox Vector3int16 type

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
t.Vector3int16 = t.typeof("Vector3int16")

--[[**
	ensures value is a given literal value

	@param literal The literal to use

	@returns A function that will return true iff the condition is passed
**--]]
function t.literal(...)
	local size = select("#", ...)
	if size == 1 then
		local literal = ...
		return function(value)
			if value ~= literal then
				return false, string.format("expected %s, got %s", tostring(literal), tostring(value))
			end

			return true
		end
	else
		local literals = {}
		for i = 1, size do
			local value = select(i, ...)
			literals[i] = t.literal(value)
		end

		return t.union(table.unpack(literals, 1, size))
	end
end

--[[**
	DEPRECATED
	Please use t.literal
**--]]
t.exactly = t.literal

--[[**
	Returns a t.union of each key in the table as a t.literal

	@param keyTable The table to get keys from

	@returns True iff the condition is satisfied, false otherwise
**--]]
function t.keyOf(keyTable)
	local keys = {}
	local length = 0
	for key in pairs(keyTable) do
		length = length + 1
		keys[length] = key
	end

	return t.literal(table.unpack(keys, 1, length))
end

--[[**
	Returns a t.union of each value in the table as a t.literal

	@param valueTable The table to get values from

	@returns True iff the condition is satisfied, false otherwise
**--]]
function t.valueOf(valueTable)
	local values = {}
	local length = 0
	for _, value in pairs(valueTable) do
		length = length + 1
		values[length] = value
	end

	return t.literal(table.unpack(values, 1, length))
end

--[[**
	ensures value is an integer

	@param value The value to check against

	@returns True iff the condition is satisfied, false otherwise
**--]]
function t.integer(value)
	local success, errMsg = t.number(value)
	if not success then
		return false, errMsg or ""
	end

	if value % 1 == 0 then
		return true
	else
		return false, string.format("integer expected, got %s", value)
	end
end

--[[**
	ensures value is a number where min <= value

	@param min The minimum to use

	@returns A function that will return true iff the condition is passed
**--]]
function t.numberMin(min)
	return function(value)
		local success, errMsg = t.number(value)
		if not success then
			return false, errMsg or ""
		end

		if value >= min then
			return true
		else
			return false, string.format("number >= %s expected, got %s", min, value)
		end
	end
end

--[[**
	ensures value is a number where value <= max

	@param max The maximum to use

	@returns A function that will return true iff the condition is passed
**--]]
function t.numberMax(max)
	return function(value)
		local success, errMsg = t.number(value)
		if not success then
			return false, errMsg
		end

		if value <= max then
			return true
		else
			return false, string.format("number <= %s expected, got %s", max, value)
		end
	end
end

--[[**
	ensures value is a number where min < value

	@param min The minimum to use

	@returns A function that will return true iff the condition is passed
**--]]
function t.numberMinExclusive(min)
	return function(value)
		local success, errMsg = t.number(value)
		if not success then
			return false, errMsg or ""
		end

		if min < value then
			return true
		else
			return false, string.format("number > %s expected, got %s", min, value)
		end
	end
end

--[[**
	ensures value is a number where value < max

	@param max The maximum to use

	@returns A function that will return true iff the condition is passed
**--]]
function t.numberMaxExclusive(max)
	return function(value)
		local success, errMsg = t.number(value)
		if not success then
			return false, errMsg or ""
		end

		if value < max then
			return true
		else
			return false, string.format("number < %s expected, got %s", max, value)
		end
	end
end

--[[**
	ensures value is a number where value > 0

	@returns A function that will return true iff the condition is passed
**--]]
t.numberPositive = t.numberMinExclusive(0)

--[[**
	ensures value is a number where value < 0

	@returns A function that will return true iff the condition is passed
**--]]
t.numberNegative = t.numberMaxExclusive(0)

--[[**
	ensures value is a number where min <= value <= max

	@param min The minimum to use
	@param max The maximum to use

	@returns A function that will return true iff the condition is passed
**--]]
function t.numberConstrained(min, max)
	assert(t.number(min))
	assert(t.number(max))
	local minCheck = t.numberMin(min)
	local maxCheck = t.numberMax(max)

	return function(value)
		local minSuccess, minErrMsg = minCheck(value)
		if not minSuccess then
			return false, minErrMsg or ""
		end

		local maxSuccess, maxErrMsg = maxCheck(value)
		if not maxSuccess then
			return false, maxErrMsg or ""
		end

		return true
	end
end

--[[**
	ensures value is a number where min < value < max

	@param min The minimum to use
	@param max The maximum to use

	@returns A function that will return true iff the condition is passed
**--]]
function t.numberConstrainedExclusive(min, max)
	assert(t.number(min))
	assert(t.number(max))
	local minCheck = t.numberMinExclusive(min)
	local maxCheck = t.numberMaxExclusive(max)

	return function(value)
		local minSuccess, minErrMsg = minCheck(value)
		if not minSuccess then
			return false, minErrMsg or ""
		end

		local maxSuccess, maxErrMsg = maxCheck(value)
		if not maxSuccess then
			return false, maxErrMsg or ""
		end

		return true
	end
end

--[[**
	ensures value matches string pattern

	@param string pattern to check against

	@returns A function that will return true iff the condition is passed
**--]]
function t.match(pattern)
	assert(t.string(pattern))
	return function(value)
		local stringSuccess, stringErrMsg = t.string(value)
		if not stringSuccess then
			return false, stringErrMsg
		end

		if string.match(value, pattern) == nil then
			return false, string.format("%q failed to match pattern %q", value, pattern)
		end

		return true
	end
end

--[[**
	ensures value is either nil or passes check

	@param check The check to use

	@returns A function that will return true iff the condition is passed
**--]]
function t.optional(check)
	assert(t.callback(check))
	return function(value)
		if value == nil then
			return true
		end

		local success, errMsg = check(value)
		if success then
			return true
		else
			return false, string.format("(optional) %s", errMsg or "")
		end
	end
end

--[[**
	matches given tuple against tuple type definition

	@param ... The type definition for the tuples

	@returns A function that will return true iff the condition is passed
**--]]
function t.tuple(...)
	local checks = { ... }
	return function(...)
		local args = { ... }
		for i, check in ipairs(checks) do
			local success, errMsg = check(args[i])
			if success == false then
				return false, string.format("Bad tuple index #%s:\n\t%s", i, errMsg or "")
			end
		end

		return true
	end
end

--[[**
	ensures all keys in given table pass check

	@param check The function to use to check the keys

	@returns A function that will return true iff the condition is passed
**--]]
function t.keys(check)
	assert(t.callback(check))
	return function(value)
		local tableSuccess, tableErrMsg = t.table(value)
		if tableSuccess == false then
			return false, tableErrMsg or ""
		end

		for key in pairs(value) do
			local success, errMsg = check(key)
			if success == false then
				return false, string.format("bad key %s:\n\t%s", tostring(key), errMsg or "")
			end
		end

		return true
	end
end

--[[**
	ensures all values in given table pass check

	@param check The function to use to check the values

	@returns A function that will return true iff the condition is passed
**--]]
function t.values(check)
	assert(t.callback(check))
	return function(value)
		local tableSuccess, tableErrMsg = t.table(value)
		if tableSuccess == false then
			return false, tableErrMsg or ""
		end

		for key, val in pairs(value) do
			local success, errMsg = check(val)
			if success == false then
				return false, string.format("bad value for key %s:\n\t%s", tostring(key), errMsg or "")
			end
		end

		return true
	end
end

--[[**
	ensures value is a table and all keys pass keyCheck and all values pass valueCheck

	@param keyCheck The function to use to check the keys
	@param valueCheck The function to use to check the values

	@returns A function that will return true iff the condition is passed
**--]]
function t.map(keyCheck, valueCheck)
	assert(t.callback(keyCheck))
	assert(t.callback(valueCheck))
	local keyChecker = t.keys(keyCheck)
	local valueChecker = t.values(valueCheck)

	return function(value)
		local keySuccess, keyErr = keyChecker(value)
		if not keySuccess then
			return false, keyErr or ""
		end

		local valueSuccess, valueErr = valueChecker(value)
		if not valueSuccess then
			return false, valueErr or ""
		end

		return true
	end
end

--[[**
	ensures value is a table and all keys pass valueCheck and all values are true

	@param valueCheck The function to use to check the values

	@returns A function that will return true iff the condition is passed
**--]]
function t.set(valueCheck)
	return t.map(valueCheck, t.literal(true))
end

do
	local arrayKeysCheck = t.keys(t.integer)
--[[**
		ensures value is an array and all values of the array match check

		@param check The check to compare all values with

		@returns A function that will return true iff the condition is passed
	**--]]
	function t.array(check)
		assert(t.callback(check))
		local valuesCheck = t.values(check)

		return function(value)
			local keySuccess, keyErrMsg = arrayKeysCheck(value)
			if keySuccess == false then
				return false, string.format("[array] %s", keyErrMsg or "")
			end

			-- # is unreliable for sparse arrays
			-- Count upwards using ipairs to avoid false positives from the behavior of #
			local arraySize = 0

			for _ in ipairs(value) do
				arraySize = arraySize + 1
			end

			for key in pairs(value) do
				if key < 1 or key > arraySize then
					return false, string.format("[array] key %s must be sequential", tostring(key))
				end
			end

			local valueSuccess, valueErrMsg = valuesCheck(value)
			if not valueSuccess then
				return false, string.format("[array] %s", valueErrMsg or "")
			end

			return true
		end
	end

--[[**
		ensures value is an array of a strict makeup and size

		@param check The check to compare all values with

		@returns A function that will return true iff the condition is passed
	**--]]
	function t.strictArray(...)
		local valueTypes = { ... }
		assert(t.array(t.callback)(valueTypes))

		return function(value)
			local keySuccess, keyErrMsg = arrayKeysCheck(value)
			if keySuccess == false then
				return false, string.format("[strictArray] %s", keyErrMsg or "")
			end

			-- If there's more than the set array size, disallow
			if #valueTypes < #value then
				return false, string.format("[strictArray] Array size exceeds limit of %d", #valueTypes)
			end

			for idx, typeFn in pairs(valueTypes) do
				local typeSuccess, typeErrMsg = typeFn(value[idx])
				if not typeSuccess then
					return false, string.format("[strictArray] Array index #%d - %s", idx, typeErrMsg)
				end
			end

			return true
		end
	end
end

do
	local callbackArray = t.array(t.callback)
--[[**
		creates a union type

		@param ... The checks to union

		@returns A function that will return true iff the condition is passed
	**--]]
	function t.union(...)
		local checks = { ... }
		assert(callbackArray(checks))

		return function(value)
			for _, check in ipairs(checks) do
				if check(value) then
					return true
				end
			end

			return false, "bad type for union"
		end
	end

--[[**
		Alias for t.union
	**--]]
	t.some = t.union

--[[**
		creates an intersection type

		@param ... The checks to intersect

		@returns A function that will return true iff the condition is passed
	**--]]
	function t.intersection(...)
		local checks = { ... }
		assert(callbackArray(checks))

		return function(value)
			for _, check in ipairs(checks) do
				local success, errMsg = check(value)
				if not success then
					return false, errMsg or ""
				end
			end

			return true
		end
	end

--[[**
		Alias for t.intersection
	**--]]
	t.every = t.intersection
end

do
	local checkInterface = t.map(t.any, t.callback)
--[[**
		ensures value matches given interface definition

		@param checkTable The interface definition

		@returns A function that will return true iff the condition is passed
	**--]]
	function t.interface(checkTable)
		assert(checkInterface(checkTable))
		return function(value)
			local tableSuccess, tableErrMsg = t.table(value)
			if tableSuccess == false then
				return false, tableErrMsg or ""
			end

			for key, check in pairs(checkTable) do
				local success, errMsg = check(value[key])
				if success == false then
					return false, string.format("[interface] bad value for %s:\n\t%s", tostring(key), errMsg or "")
				end
			end

			return true
		end
	end

--[[**
		ensures value matches given interface definition strictly

		@param checkTable The interface definition

		@returns A function that will return true iff the condition is passed
	**--]]
	function t.strictInterface(checkTable)
		assert(checkInterface(checkTable))
		return function(value)
			local tableSuccess, tableErrMsg = t.table(value)
			if tableSuccess == false then
				return false, tableErrMsg or ""
			end

			for key, check in pairs(checkTable) do
				local success, errMsg = check(value[key])
				if success == false then
					return false, string.format("[interface] bad value for %s:\n\t%s", tostring(key), errMsg or "")
				end
			end

			for key in pairs(value) do
				if not checkTable[key] then
					return false, string.format("[interface] unexpected field %q", tostring(key))
				end
			end

			return true
		end
	end
end

--[[**
	ensure value is an Instance and it's ClassName matches the given ClassName

	@param className The class name to check for

	@returns A function that will return true iff the condition is passed
**--]]
function t.instanceOf(className, childTable)
	assert(t.string(className))

	local childrenCheck
	if childTable ~= nil then
		childrenCheck = t.children(childTable)
	end

	return function(value)
		local instanceSuccess, instanceErrMsg = t.Instance(value)
		if not instanceSuccess then
			return false, instanceErrMsg or ""
		end

		if value.ClassName ~= className then
			return false, string.format("%s expected, got %s", className, value.ClassName)
		end

		if childrenCheck then
			local childrenSuccess, childrenErrMsg = childrenCheck(value)
			if not childrenSuccess then
				return false, childrenErrMsg
			end
		end

		return true
	end
end

t.instance = t.instanceOf

--[[**
	ensure value is an Instance and it's ClassName matches the given ClassName by an IsA comparison

	@param className The class name to check for

	@returns A function that will return true iff the condition is passed
**--]]
function t.instanceIsA(className, childTable)
	assert(t.string(className))

	local childrenCheck
	if childTable ~= nil then
		childrenCheck = t.children(childTable)
	end

	return function(value)
		local instanceSuccess, instanceErrMsg = t.Instance(value)
		if not instanceSuccess then
			return false, instanceErrMsg or ""
		end

		if not value:IsA(className) then
			return false, string.format("%s expected, got %s", className, value.ClassName)
		end

		if childrenCheck then
			local childrenSuccess, childrenErrMsg = childrenCheck(value)
			if not childrenSuccess then
				return false, childrenErrMsg
			end
		end

		return true
	end
end

--[[**
	ensures value is an enum of the correct type

	@param enum The enum to check

	@returns A function that will return true iff the condition is passed
**--]]
function t.enum(enum)
	assert(t.Enum(enum))
	return function(value)
		local enumItemSuccess, enumItemErrMsg = t.EnumItem(value)
		if not enumItemSuccess then
			return false, enumItemErrMsg
		end

		if value.EnumType == enum then
			return true
		else
			return false, string.format("enum of %s expected, got enum of %s", tostring(enum), tostring(value.EnumType))
		end
	end
end

do
	local checkWrap = t.tuple(t.callback, t.callback)

--[[**
		wraps a callback in an assert with checkArgs

		@param callback The function to wrap
		@param checkArgs The function to use to check arguments in the assert

		@returns A function that first asserts using checkArgs and then calls callback
	**--]]
	function t.wrap(callback, checkArgs)
		assert(checkWrap(callback, checkArgs))
		return function(...)
			assert(checkArgs(...))
			return callback(...)
		end
	end
end

--[[**
	asserts a given check

	@param check The function to wrap with an assert

	@returns A function that simply wraps the given check in an assert
**--]]
function t.strict(check)
	return function(...)
		assert(check(...))
	end
end

do
	local checkChildren = t.map(t.string, t.callback)

--[[**
		Takes a table where keys are child names and values are functions to check the children against.
		Pass an instance tree into the function.
		If at least one child passes each check, the overall check passes.

		Warning! If you pass in a tree with more than one child of the same name, this function will always return false

		@param checkTable The table to check against

		@returns A function that checks an instance tree
	**--]]
	function t.children(checkTable)
		assert(checkChildren(checkTable))

		return function(value)
			local instanceSuccess, instanceErrMsg = t.Instance(value)
			if not instanceSuccess then
				return false, instanceErrMsg or ""
			end

			local childrenByName = {}
			for _, child in ipairs(value:GetChildren()) do
				local name = child.Name
				if checkTable[name] then
					if childrenByName[name] then
						return false, string.format("Cannot process multiple children with the same name %q", name)
					end

					childrenByName[name] = child
				end
			end

			for name, check in pairs(checkTable) do
				local success, errMsg = check(childrenByName[name])
				if not success then
					return false, string.format("[%s.%s] %s", value:GetFullName(), name, errMsg or "")
				end
			end

			return true
		end
	end
end

local slicefun = function (sequence, start, stop, step) -- slice
	local sliced = { }
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
		local fake = newproxy(true)

		setmetatable(fake, {
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
				return input[index]
			end,
			__newindex = function(self, index, value)
				input[index] = value
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
		return fake
	else
		return input
	end
end
function list(input)
	if type(input) == "table" then
		local fake = input

		setmetatable(fake, {
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
		return fake
	else
		return input
	end
end
function dict(input)
	if type(input) == "table" then
		local fake = input

		setmetatable(fake, {
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
		return fake
	else
		return input
	end
end

-- Make a directory system called py
local py = {}
local submeta = function(selfinstacnce)
	return {
		__index = function(self, index)
			-- Check if that is an instance inside of game
			local instance = selfinstacnce:FindFirstChild(index)
			if instance then
				return instance
			end
			local property = selfinstacnce[index]
			if property then
				if type(property) == "RBXScriptSignal" then
					-- return a wrapped version of property than when called it will :Connect
					local meta = {}
					meta.__call = function(self, callback)
						return property:Connect(callback)
					end
					meta.__index = function(self, index)
						if index == "Connect" then
							error("RBXScriptSignals should be called, not indexed by Connect")
						end
						return property[index]
					end

					return setmetatable({}, meta)
				end
				if type(property) == "table" then
					return list(property)
				end
				if type(property) == "string" then
					return string_meta(property)
				end
				return property
			else
				error("No such property, instance, or event called " .. index)
			end
		end,
		__newindex = function(self, index, value)
			error("Cannot set " .. index .. " to " .. value)
		end,
	}
end
local meta = {
	__index = function(self, index)
		-- Check if that is an instance inside of game
		local instance = game:FindFirstChild(index)
		if instance then
			-- wrap instance with submeta
			return setmetatable({}, submeta(instance))
		end
		local property = game[index]
		if property then
			if type(property) == "RBXScriptSignal" then
				-- return a wrapped version of property than when called it will :Connect
				local meta = {}
				meta.__call = function(self, callback)
					return property:Connect(callback)
				end
				meta.__index = function(self, index)
					if index == "Connect" then
						error("RBXScriptSignals should be called, not indexed by Connect")
					end
					return property[index]
				end

				return setmetatable({}, meta)
			end
			return property
		else
			error("No such property, instance, or event called " .. index)
		end
	end,
	__newindex = function(self, index, value)
		error("Cannot set " .. index .. " to " .. value)
	end,
}
setmetatable(py, meta)

-- Lua's table references
local sort = table.sort
local insert, remove, move = table.insert, table.remove, table.move
local pack, unpack, concat = table.pack, table.unpack, table.concat
local random = math.random
local foreach, foreachi = table.foreach, table.foreachi

-- Luau's table references
local tfind = table.find
local getn, create = table.getn, table.create
local clear = table.clear

-- New table
local table = {}

-- Private methods
local function tableCheck(v)
    return type(v) == 'table'
end

-- Public Methods

-- Returns the total number of the element in a table.
function table.count(tbl)
    local n = 0
    for _ in pairs(tbl) do
        n = n + 1
    end
    return n
end

-- Returns the total number of the element in a table recursively.
function table.deepCount(tbl)
    local n = 0
    for _, v in pairs(tbl) do
        n = type(v) == 'table' and n + table.deepCount(v) or n + 1
    end
    return n
end

-- Determines whether the table contains a value, returning `true` or `false` as appropriate.
function table.includes(tbl, value)
    for _, v in next, tbl do
        if v == value then return true end
    end
    return false
end

-- Determines if the `tbl` has `index` on it, returning `true` or `false` as appropriate.
function table.has(tbl, index)
    return tbl[index] ~= nil
end

-- Determines if the table is empty. Returns `true` or `false`, as appropriate.
function table.isEmpty(tbl)
    return next(tbl) == nil
end

-- Determines if the table is a array-like table.
function table.isArray(tbl)

    -- Make sure it's not empty.
    if table.isEmpty(tbl) then
        return false
    end

    -- Make sure that all keys are positive integers
    for key, value in pairs(tbl) do
        if type(key) ~= 'number' or key % 1 ~= 0 or key < 1 then
            return false
        end
    end

    return true
end

-- Determines if the table is a dictionary-like table.
-- A dictionary is defined as a table containing keys that are not positive integers.
function table.isDictionary(tbl)
    return not table.isArray(tbl)
end

-- Returns a new copy of the table, one layer deep.
function table.copy(tbl)
    local ret = {}
    for k, v in pairs(tbl) do
        ret[k] = v
    end
    return ret
end

--[[
Returns a copy of table, recursively.
If a table is encountered, it is recursively deep-copied.
Metatables are not copied.
]]
function table.deepCopy(tbl)
    local ret = {}
    for k, v in pairs(tbl) do
        ret[k] = type(v) == 'table' and table.deepCopy(v) or v
    end
    return ret
end

-- Reverses the element of an array-like table in place.
function table.reverse(tbl)
    if table.isEmpty(tbl) then
        error('`tbl` must not be empty!', 2)
    elseif table.isDictionary(tbl) then
        error('`tbl` must be a array-like table!', 2)
    end

    for i = 1, #tbl do
        insert(tbl, i, remove(tbl))
    end
end

-- Returns a copy of an array-like table with its element in reverse order.
-- The original table remain unchanged.
function table.reversed(tbl)
    if table.isEmpty(tbl) then
        error('`tbl` must not be empty!', 2)
    elseif table.isDictionary(tbl) then
        error('`tbl` must be a array-like table!', 2)
    end

    local ret = {}
    for i = #tbl, 1, -1 do
        insert(ret, tbl[i])
    end
    return ret
end

-- Returns a new array-like table where all of its values are the keys of the original table.
function table.keys(tbl)
    local ret = {}
    for k in pairs(tbl) do
        insert(ret, k)
    end
    return ret
end

-- Returns a new array-like table where all of its values are the values of the original table.
function table.values(tbl)
    local ret = {}
    for _, v in pairs(tbl) do
        insert(ret, v)
    end
    return ret
end

-- Returns a random (index, value) pair from an array-like table.
function table.randomIpair(tbl)
    local i = random(#tbl)
    return i, tbl[i]
end

-- Returns a random (key, value) pair from a dictionary-like table.
function table.randomPair(tbl)
    local rand = random(table.count(tbl))
    local n = 0
    for k, v in pairs(tbl) do
        n = n + 1
        if n == rand then
            return k, v
        end
    end
end

-- Returns a copy of an array-like table sorted using Lua's `table.sort`.
function table.sorted(tbl, fn)
    local ret = {}
    for i, v in ipairs(tbl) do
        ret[i] = v
    end
    sort(ret, fn)
    return ret
end

-- Returns a new table that is a slice of the original, defined by the start and stop bounds and the step size.
-- Default start, stop, and step values are 1, #tbl, and 1 respectively.
function table.slice(tbl, start, stop, step)
    local ret = {}
    for i = start or 1, stop or #tbl, step or 1 do
        insert(ret, tbl[i])
    end
    return ret
end

-- Iterates through a table until a value satisfies the test function.
-- The `value` is returned if it satisfies the test function. Otherwise, `nil` is returned.
function table.findValue(tbl, testFn)
    for key, value in pairs(tbl) do
        if testFn(value, key) == true then
            return value
        end
    end
    return nil
end

-- Iterates through a table until a key satisfies the test function.
-- The `key` is returned if it satisfies the test function. Otherwise, `nil` is returned.
function table.findIndex(tbl, testFn)
    for key, value in pairs(tbl) do
        if testFn(value, key) == true then
            return key
        end
    end
    return nil
end

-- Returns a new table containing all elements of the calling table
-- for which provided filtering function returns `true`.
function table.filter(tbl, filterFn)
    local ret = {}
    for key, value in pairs(tbl) do
        if filterFn(value, key) then
            ret[key] = value
        end
    end
    return ret
end

-- Returns a new table containing the results of calling a function
-- on every element in this table.
function table.map(tbl, mapFn)
    local ret = {}
    for key, value in pairs(tbl) do
        ret[key] = mapFn(value, key)
    end
    return ret
end

-- Iterates through the table and run the test function to to every element to check if it satisfies the check.
-- If all elements satisfies the check, it returns `true`. Otherwise it returns `false`.
function table.every(tbl, testFn)
    for key, value in pairs(tbl) do
        if testFn(value, key) == false then
            return false
        end
    end
    return true
end

-- Returns a new table that is this table joined with other table(s).
function table.merge(...)
    local ret = {}
    local tables = {...}
    
    if not table.every(tables, tableCheck) then
        error('`...table` must be a table!', 2)
    end

    for _, t in pairs(tables) do
        for k, v in pairs(t) do
            if type(k) == 'number' then
                insert(ret, v)
            else
                ret[k] = v
            end
        end
    end

    return ret
end

-- Changes all elements in an array-like table to a static value
-- from start index (default: `1`) to an end index (default: `#tbl`).
-- It returns the modified array-like table.
function table.fill(tbl, value, start, End)
    if table.isEmpty(tbl) then
        error('`tbl` must not be empty!', 2)
    elseif table.isDictionary(tbl) then
        error('`tbl` must be a array-like table!', 2)
    elseif start ~= nil and start <= 0 then
        error('`start` must be more than 0!', 2)
    elseif End ~= nil and End > #tbl then
        error('`End` must not exceed #tbl!', 2)
    end

    for i = start or 1, End or #tbl do
        tbl[i] = value
    end

    return tbl
end

-- Returns a new copy of the original array-like table and removes duplicate elements that exists on that table.
function table.removeDupes(tbl)
    if table.isEmpty(tbl) then
        error('`tbl` must not be empty!', 2)
	elseif table.isDictionary(tbl) then
	    error('`tbl` must be a array-like table!', 2)
    end

    local hash = {}
    local ret = {}
    for _,v in ipairs(tbl) do
        if not hash[v] then
            insert(ret, v)
            hash[v] = true
        end
    end

	return ret
end

--{SOURCECODEGOESHERE}--

local libraries = {
	["example"] = function() print("Example library!") end,
	--{ITEMSGOHERE}--
}
local dependenciesfolder = script.Parent

local module = function(scriptname)
	return { 
		py = {
			pylib,
			function(index, sub) -- import
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
			end,
			{ -- python built in
				stringmeta = string_meta, list = list, dict = dict, -- class meta
				python = function(input) 
					return createProxy(input) 
				end, -- python()
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
				__name__ = if script:IsA("BaseScript") then "__main__" else script.Name , 
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
				open = function (filename, mode) --open
					if not io then error("io is not enabled") end
					return io.open(filename, mode)
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
				exec = function (code, env)
					return loadstring(expr)
				end,

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
				bin = function (number) -- bin
					return string.format("%b", number)
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

					print("Breakpoint hit!")
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
				compile = function (source, filename, mode) -- compile
					-- This is a placeholder implementation and might not cover all possible use cases.
					-- You would need to provide your own implementation based on your specific requirements.
					-- Here's an example of a simple compilation to execute Lua code directly:
					local compiledFunction = loadstring(source, filename)
					return compiledFunction
				end,


				-- help()
				help = function (object) -- help
					-- This is a placeholder implementation and might not cover all possible use cases.
					-- You would need to provide your own implementation based on your specific requirements.
					-- Here's an example of displaying a help message for an object:
					print("Help for object:", object)
					print("Type:", type(object))
					-- Add more information or documentation here
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
			},
		},
		lunar = {
			function(index, sub) -- import
				if libraries[index] then
					if sub then
						return libraries[index][sub]
					else
						return libraries[index]
					end
				elseif script.Parent:FindFirstChildOfClass("ModuleScript") then
					return require(script.Parent:FindFirstChildOfClass("ModuleScript"))
				elseif script.Parent:FindFirstChildOfClass("Folder") then
					return require(script.Parent:FindFirstChildOfClass("Folder"):FindFirstChild("init") or script.Parent:FindFirstChildOfClass("Folder"):FindFirstChild(sub) or error("No such library called " .. index.." and no init file found either"))
				else
					error("No such library called " .. index)
				end
			end,
			{-- lunar built in
				type = t,
				table = table,
			},
		},
		c = {
			function(index, sub) -- import
				if libraries[index] then
					if sub then
						return libraries[index][sub]
					else
						return libraries[index]
					end
				elseif script.Parent:FindFirstChildOfClass("ModuleScript") then
					return require(script.Parent:FindFirstChildOfClass("ModuleScript"))
				elseif script.Parent:FindFirstChildOfClass("Folder") then
					return require(script.Parent:FindFirstChildOfClass("Folder"):FindFirstChild("init") or script.Parent:FindFirstChildOfClass("Folder"):FindFirstChild(sub) or error("No such library called " .. index.." and no init file found either"))
				else
					error("No such library called " .. index)
				end
			end,
			{-- c and c++ built in
			}
		}
	}
end



_G.pyc = module