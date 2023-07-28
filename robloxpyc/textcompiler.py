import json
import os
import sys
if not (os.path.dirname(os.path.abspath(__file__)).startswith(sys.path[-1])):
    from errormanager import *
    from util import *
else:
    from .errormanager import *
    from .util import *


def json_to_lua(json_str):
    data = json.loads(json_str)
    return _json_to_lua(data)

def _json_to_lua(data):
    if isinstance(data, dict):
        items = []
        for key, value in data.items():
            items.append('[{}] = {}'.format(_json_to_lua(key), _json_to_lua(value)))
        return '{{{}}}'.format(', '.join(items))
    elif isinstance(data, list):
        items = []
        for value in data:
            items.append(_json_to_lua(value))
        return '{{{}}}'.format(', '.join(items))
    elif isinstance(data, str):
        return '"{}"'.format(data)
    else:
        return str(data)


def unknowncompile(r, file):
  if file.endswith(".txt") or ("." not in file):
     # This is for text files and files without a file extension
    try:
      contents = ""
      with open(os.path.join(r, file), "r") as f:
        contents = f.read()
        contents = contents.replace("]]", "]\]")
        contents = "--/ Compiled using roblox-pyc | Textfile compiler \--\nlocal file\nfile = {Contents = [["+contents+"]], Type = 'rawtext', Extension = '"+file.split(".")[file.split(".").__len__()-1]+"', SetSource = function(self, input) self.Contents = input end}"
        filename = os.path.basename(file)
        sepratedbydot = filename.split(".")
        ending = sepratedbydot[sepratedbydot.__len__()-1]
        newfilename = filename.replace("."+ending, ".lua")
        # if newfilename == oldfilename, add .lua to the end. For files without endings
        if filename == newfilename:
          newfilename = newfilename+".lua"
                  
        open(os.path.join(r, newfilename), "x").close()
        with open(os.path.join(r, newfilename), "w") as f:
          f.write(contents)
    except UnicodeDecodeError:
        print(warn("Failed to read "+os.path.join(r, file)+"!"))
def jsoncompile(r, file):
  if file.endswith(".json"):
    # compile the file to a file with the same name and path but .lua
    try:
      contents = ""
      with open(os.path.join(r, file), "r") as f:
        contents = f.read()
        contents = "--/ Compiled using roblox-pyc | JSON compiler \--\nreturn {Contents = "+json_to_lua(contents)+", Type = 'json', Extension = 'json', SetSource = function(self, input) self.Contents = input end}"
        filename = os.path.basename(file)
        sepratedbydot = filename.split(".")
        ending = sepratedbydot[sepratedbydot.__len__()-1]
        newfilename = filename.replace("."+ending, ".lua")
        # if newfilename == oldfilename, add .lua to the end. For files without endings
        if filename == newfilename:
          newfilename = newfilename+".lua"
        if not os.path.exists(os.path.dirname(os.path.join(r, newfilename))):
          open(os.path.join(r, newfilename), "x").close()
        with open(os.path.join(r, newfilename), "w") as f:
          f.write(contents)
    except UnicodeDecodeError:
        # Just delete the file
        print(warn("Failed to read "+os.path.join(r, file)+"!"))
def othercompile(r, file): # Handles Text files and JSON files, and files without a file extension
  jsoncompile(r, file)
  unknowncompile(r, file)