headertemplate = """--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local py, import, builtin = _G.pyc(script).py

{}
-----------------------------------------------------------------------------
"""
lunarheadertemplate = """--/ Compiled using roblox-pyc | Lunar compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
repeat task.wait() until _G.pyc
local import, builtin = _G.pyc(script).lunar

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