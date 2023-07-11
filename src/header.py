headertemplate = """
--// Compiled using roblox-pyc \\--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

{}
-----------------------------------------------------------------------------
"""

def header(functions):
    code = ""
    for i in functions:
        code += "local "+i+" = builtin."+i+"\n"
    
    #print(code)
    return headertemplate.format(code)