--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = _G.pyc.py

local stringmeta = builtin.stringmeta
local str = builtin.str
local match = builtin.match
local int = builtin.int

-----------------------------------------------------------------------------
local x = stringmeta "10"
match(x, {
[10] = function()
    print(stringmeta "x is 10")
end,
[20] = function()
    print(stringmeta "x is 20")
end,
["default"] = function()
    print(stringmeta "x is not 10 or 20")
end,
})