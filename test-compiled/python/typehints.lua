--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local sum = builtin.sum
local int = builtin.int
local stringmeta = builtin.stringmeta
local str = builtin.str

-----------------------------------------------------------------------------
local function sum_numbers(a, b)
    return (a + b)
end
print(sum_numbers(10, 5))
print(sum_numbers(10.3, 5))
print(sum_numbers(stringmeta "Bob", stringmeta "Mark"))