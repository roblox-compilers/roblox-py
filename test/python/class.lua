--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local class = builtin.class
local int = builtin.int
local stringmeta = builtin.stringmeta
local str = builtin.str

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
local new = Example(stringmeta "John")
new.print_name()
new.sethobby(stringmeta "Roblox Game Development")
new.printhobby()