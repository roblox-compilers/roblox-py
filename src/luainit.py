import os
import pip
import sys

initcode = ""

try:
	with open("src/luainitlua.lua", "r") as f:
		initcode = f.read()
except FileNotFoundError:
    print("roblox-pyc: Due to a bug, lib will not work, please report this issue to the github repo, discord server, or the devforum post\nthanks!")
allfunctions = "stringmeta, list, dict, python, staticmethod, classsmethod, class, range, __name__, len, abs, str, int, sum, max, min, reversed, split, round, all, any, ord, char, callable, zip, float, format, hex, id, map, bool, divmod, slice, operator_in, asynchronousfunction, match, anext, ascii, dir, getattr, globals, hasattr, input, isinstance, issubclass, iter, locals, oct, open, ord, pow, eval, exec, filter, frozenset, aiter, bin, complex, delattr, enumerate, breakpoint, bytearray, bytes, compile, help, memoryview, repr, sorted, vars, __import_, formatmod"
lunarfunctions = "type, table"
allfunctions = allfunctions.split(", ")
lunarfunctions = lunarfunctions.split(", ")

def generatewithlibraries ():
	libraries = "{"
	files = ""
    
    # add it so it would be organized like so:
    # {x = {y = {z = {contents = "contents", name = "name"}}}}
    # using os.walk, check where the pip libraries are stored
    
	pipfolder = os.path.join(os.path.dirname(sys.executable), "Lib", "site-packages")
    
	for root, dirs, files in os.walk(pipfolder):
		newline = "[\"{}\"] = {".format(root)
		for file in files:
			newline += "[\"{}\"] = {{contents = [[{}]], name = \"{}\"}},".format(file, open(os.path.join(root, file)).read(), file)
		newline += "},"
  
	files = newline
    
    # check all libraries that pip has installed
	for lib in pip.get_installed_distributions():
		libraries += "{}, ".format(lib.key)
    
	libraries += "}"
    
	print(libraries, files)
	#return initcode.format(libs = libraries)
