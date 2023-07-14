--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local stringmeta = builtin.stringmeta
local str = builtin.str
local int = builtin.int
local format = builtin.format
local exec = builtin.exec
local formatmod = builtin.formatmod
local staticmethod = builtin.staticmethod
local class = builtin.class

-----------------------------------------------------------------------------
local function foo(x)
    print((formatmod(stringmeta "executing foo(%s)", x)))
end
foo = staticmethod(foo)
local A = class(function(A)
    A.foo = foo
    return A
end, {})
local a = A()
a.foo(stringmeta "hi")