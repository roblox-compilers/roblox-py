headertemplate = """--// Compiled using roblox-pyc \\--
		
		
------------------------------------ BUILT IN -------------------------------
local py, libs, builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).py)

{}
-----------------------------------------------------------------------------
"""
lunarheadertemplate = """--// Compiled using roblox-pyc \\--
		
		
------------------------------------ BUILT IN -------------------------------
local builtin = unpack(require(game.ReplicatedStorage["roblox.pyc"])(script).lunar)

{}
-----------------------------------------------------------------------------
"""


def header(functions):
    code = ""
    for i in functions:
        code += "local "+i+" = builtin."+i+"\n"
    
    #print(code)
    return headertemplate.format(code)

def lunarheader(functions):
    code = ""
    for i in functions:
        code += "local "+i+" = builtin."+i+"\n"
    
    #print(code)
    return lunarheadertemplate.format(code)