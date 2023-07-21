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
allfunctions = "stringmeta, list, dict, python, staticmethod, classsmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice, operator_in, asynchronousfunction, match, anext, ascii, dir, getattr, globals, hasattr, input, isinstance, issubclass, iter, locals, oct, open, ord, pow, eval, exec, filter, frozenset, aiter, bin, complex, delattr, enumerate, breakpoint, bytearray, bytes, compile, help, memoryview, repr, sorted, vars, __import_, formatmod"
lunarfunctions = "type, table"
allfunctions = allfunctions.split(", ")
lunarfunctions = lunarfunctions.split(", ")

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
        itemstext += f'"{list(items.keys())[i]}" = {list(items.values())[i]}\n'
	
    currentcode = currentcode.replace("--{SOURCECODEGOESHERE}--", sourcestext)
    currentcode = currentcode.replace("--{ITEMSGOHERE}--", itemstext)
 
    return currentcode
