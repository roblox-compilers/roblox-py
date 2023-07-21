--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local range = builtin.range

-----------------------------------------------------------------------------
for i in range(10) do
    if (i == 5) then
        continue
    end
end