--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).lunar)

local type = builtin.type
local table = builtin.table

-----------------------------------------------------------------------------
local count_to_10
count_to_10 = function()
  for i in 1,10 do
    print(i)
  end
end
count_to_10()
for i in 5,10 do
  print(i)
end
return print("Hello World")
