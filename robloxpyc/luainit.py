import os
import pip
import sys
from . import colortext as colortext

initcode = ""

try:
    # check for a luainitlua.lua file from the same directory as this file
	with open(os.path.join(os.path.dirname(__file__), "luainitlua.lua")) as f:
		initcode = f.read()
except FileNotFoundError:
    print(colortext.yellow("warning", ["bold"])+" Due to a bug, lib will not work, please report this issue to the github repo, discord server, or the devforum post\nthanks!")
allfunctions = "safeadd, list, dict, python, staticmethod, classsmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice, operator_in, asynchronousfunction, match, anext, ascii, dir, getattr, globals, hasattr, input, isinstance, issubclass, iter, locals, oct, open, ord, pow, eval, exec, filter, frozenset, aiter, bin, complex, delattr, enumerate, breakpoint, bytearray, bytes, compile, help, memoryview, repr, sorted, vars, __import_, formatmod"
lunarfunctions = ""
robloxfunctions = """["assert"] = "function",
	["error"] = "function",
	["getfenv"] = "function",
	["getmetatable"] = "function",
	["ipairs"] = "function",
	["loadstring"] = "function",
	["newproxy"] = "function",
	["next"] = "function",
	["pairs"] = "function",
	["pcall"] = "function",
	["print"] = "function",
	["rawequal"] = "function",
	["rawget"] = "function",
	["rawlen"] = "function",
	["rawset"] = "function",
	["select"] = "function",
	["setfenv"] = "function",
	["setmetatable"] = "function",
	["tonumber"] = "function",
	["tostring"] = "function",
	["unpack"] = "function",
	["xpcall"] = "function",
	["collectgarbage"] = "function",
	["_G"] = "table",
	["_VERSION"] = "string",
	["bit32"] = "table",
	["coroutine"] = "table",
	["debug"] = "table",
	["math"] = "table",
	["os"] = "table",
	["string"] = "table",
	["table"] = "table",
	["utf8"] = "table",
	["DebuggerManager"] = "function",
	["delay"] = "function",
	["gcinfo"] = "function",
	["PluginManager"] = "function",
	["require"] = "function",
	["settings"] = "function",
	["spawn"] = "function",
	["tick"] = "function",
	["time"] = "function",
	["UserSettings"] = "function",
	["wait"] = "function",
	["warn"] = "function",
	["Delay"] = "function",
	["ElapsedTime"] = "function",
	["elapsedTime"] = "function",
	["printidentity"] = "function",
	["Spawn"] = "function",
	["Stats"] = "function",
	["stats"] = "function",
	["Version"] = "function",
	["version"] = "function",
	["Wait"] = "function",
	["ypcall"] = "function",
	["game"] = "Instance",
	["plugin"] = "Instance",
	["script"] = "Instance",
	["shared"] = "Instance",
	["workspace"] = "Instance",
	["Game"] = "Instance",
	["Workspace"] = "Instance",
	["Axes"] = "table",
	["BrickColor"] = "table",
	["CatalogSearchParams"] = "table",
	["CFrame"] = "table",
	["Color3"] = "table",
	["ColorSequence"] = "table",
	["ColorSequenceKeypoint"] = "table",
	["DateTime"] = "table",
	["DockWidgetPluginGuiInfo"] = "table",
	["Enum"] = "table",
	["Faces"] = "table",
	["FloatCurveKey"] = "table",
	["Font"] = "table",
	["Instance"] = "table",
	["NumberRange"] = "table",
	["NumberSequence"] = "table",
	["NumberSequenceKeypoint"] = "table",
	["OverlapParams"] = "table",
	["PathWaypoint"] = "table",
	["PhysicalProperties"] = "table",
	["Random"] = "table",
	["Ray"] = "table",
	["RaycastParams"] = "table",
	["Rect"] = "table",
	["Region3"] = "table",
	["Region3int16"] = "table",
	["RotationCurveKey"] = "table",
	["SharedTable"] = "table",
	["task"] = "table",
	["TweenInfo"] = "table",
	["UDim"] = "table",
	["UDim2"] = "table",
	["Vector2"] = "table",
	["Vector2int16"] = "table",
	["Vector3"] = "table",
	["Vector3int16"] = "table",
"""
allfunctions = allfunctions.split(", ")
lunarfunctions = lunarfunctions.split(", ")

# Parse robloxfunctions to something that looks like allfunctions
robloxfunctions = robloxfunctions.replace("\n", "").replace("\t", "").replace(" ", "").replace('"', "").replace("'", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").split(",")
for i in range(len(robloxfunctions)):
    item = robloxfunctions[i]
    if item == "":
        # Remove from list
        robloxfunctions.pop(i)
    else:
        # Split by = and the first item is the name
        robloxfunctions[i] = item.split("=")[0]

def generatewithlibraries (libs):
    # Every item in libs is a table with 3 values
    # name (what to download by)
    # data (source code)
    # var (what variable is the source code stored in)
    
    # The initcode has 2 comments, --{SOURCECODEHERE}-- and --{ITEMSHERE}--. Replace SOURCECODEHERE with all of the source codes seprated by newlines
    # and for ITEMSHERE, "<name>" = <var>
    
    currentcode = initcode
    sources = []
    items = {}
    
    for i in range(len(libs)):
        sources.append(libs[i]["data"])
        items[libs[i]["name"]] = libs[i]["var"]
    
    sourcestext = "\n".join(sources)
    itemstext = ""
    
    for i in range(len(items)):
        itemstext += f'["{list(items.keys())[i]}"] = {list(items.values())[i]}\n'
	
    currentcode = currentcode.replace("--{SOURCECODEGOESHERE}--", sourcestext)
    currentcode = currentcode.replace("--{ITEMSGOHERE}--", itemstext)
 
    return currentcode
