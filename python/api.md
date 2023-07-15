---
description: How can you use the built in API.
---

# API

Use the&#x20;

```
py
```

variable to access the game in python, This is equivalent to game in roblox.

<pre class="language-python"><code class="lang-python"><strong>ValidPlayers = [
</strong><strong>    "builderman"
</strong><strong>]
</strong><strong>
</strong>@py.Workspace.Spawn.Touched
<strong>def onTouch(touch):
</strong>    print("Spawn has been touched by", touch.Name)
    
@py.Players.PlayerAdded
def onPlrAdd(plr):
    if plr.Name in ValidPlayers:
        # The player is in our admin list, print admin joined
        print("Admin", plr.Name, "has joined the game!!")
        
</code></pre>

The above code will do the following:

* When a part in workspace called "Spawn" is touched print the touching parts name in the output
* When a player joins and their name is in the ValidPlayers list that means they are a admin and output that&#x20;

Compiled code:

```lua
--// Compiled using roblox-pyc \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

local stringmeta = builtin.stringmeta
local list = builtin.list
local str = builtin.str
local id = builtin.id
local int = builtin.int
local operator_in = builtin.operator_in
local min = builtin.min

-----------------------------------------------------------------------------
local ValidPlayers = list {stringmeta "builderman"}
local function onTouch(touch)
    print(stringmeta "Spawn has been touched by", touch.Name)
end
onTouch = py.Workspace.Spawn.Touched(onTouch)
local function onPlrAdd(plr)
    if (operator_in(plr.Name, ValidPlayers)) then
        print(stringmeta "Admin", plr.Name, stringmeta "has joined the game!!")
    end
end
onPlrAdd = py.Players.PlayerAdded(onPlrAdd)
```



***

Check out the tests in github
