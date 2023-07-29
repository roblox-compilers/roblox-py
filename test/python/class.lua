--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

local class = builtin.class
local int = builtin.int
local print = builtin.print
local Game = builtin.Game

-----------------------------------------------------------------------------
local Example = class(function(Example)
    function Example.__init__(self, name)
        self.name = name
    end
    function Example.print_name(self)
        print(self.name)
    end
    function Example.sethobby(self, hobby)
        self.hobby = hobby
    end
    function Example.printhobby(self)
        print(self.hobby)
    end
    function Example.setage(self, age)
        self.age = age
    end
    function Example.printage(self)
        print(self.age)
    end
    return Example
end, {})
local new = Example("John")
new.print_name()
new.sethobby("Roblox Game Development")
new.printhobby()

------------------------------------ END ------------------------------------
if script:IsA("ModuleScript") then 
	return getfenv()
else
	repeat task.wait() until _G.pyc
	_G.pyc.libs[script] = getfenv()
end
------------------------------------ END ------------------------------------

