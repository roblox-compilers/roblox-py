
--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local range = builtin.range

-----------------------------------------------------------------------------
for i in range(10) do
    if (i == 5) then
        continue 8
    end
end