"""Holds many useful functions for roblox-pyc"""
import sys
if not (os.path.dirname(os.path.abspath(__file__)).startswith(sys.path[-1])):
    import colortext, configmanager, pytranslator
else:
    from . import colortext, configmanager, pytranslator
import os

def backwordreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)
def filtercompiledfolder():
  cwd = os.getcwd()
  compiled = cwd+"-compiled"
  for r, d, f in os.walk(compiled):
    for file in f:
      if not file.endswith(".lua"):
        os.remove(os.path.join(r, file))

def onNotFound(target):
  currentcommand = sys.argv[2]
  
  allCLIS = configmanager.getconfig("general", "cli", [])
  
  # go through allCLIS and check if target and command matches
  for i in allCLIS:
    if i["target"] == target:
      pass
def lib():
    # if /server and /client are found, then error
    if os.path.exists(os.path.join(os.getcwd(), "server")) and os.path.exists(os.path.join(os.getcwd(), "client")):
      print(colortext.warn("Do not install dependencies inside of the parent folder, rather both the /server and /client folder. Would you like to do this?"))
      inputval = input("[Y/n]: ").lower()
      if inputval == "n":
        sys.exit()
      elif inputval == "y":
        # Set cwd to server and run lib
        os.chdir(os.path.join(os.getcwd(), "server"))
        lib()
        # set cwd to client and run lib
        os.chdir(os.path.join(os.getcwd(), "..", "client"))
        lib()
    # create dependencies folder if it doesnt exist
    if not os.path.exists(os.path.join(os.getcwd(), "dependencies")):
      os.makedirs(os.path.join(os.getcwd(), "dependencies"))
  
    cwd = os.getcwd()
    # cwd+sys.argv[2]
    dir = os.path.join(cwd,"dependencies", "stdlib.lua")
    if not os.path.exists(os.path.dirname(dir)):
        open(dir, "x").close()
    with open(dir, "w") as f:
        translator = pytranslator.Translator()
        f.write(translator.get_luainit(configmanager.getconfig("general", "luaext", [])))
    # Make a file called content.json in the dependencies folder
    open(os.path.join(cwd, "dependencies", "content.json"), "x").close()
