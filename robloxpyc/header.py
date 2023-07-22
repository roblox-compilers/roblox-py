headertemplate = """--/ Compiled using roblox-pyc | Python compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local py, import, builtin = _G.pyc.py

{}
-----------------------------------------------------------------------------
"""
lunarheadertemplate = """--/ Compiled using roblox-pyc | Lunar compiler \--
		
		
------------------------------------ BUILT IN -------------------------------
local import, builtin = _G.pyc.lunar

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