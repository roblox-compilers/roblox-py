"""Handles the main interface"""

# PYPI 
from flask import Flask, request
from pyflakes import api
from packaging import version
from tqdm import tqdm
from time import sleep

# FILES
if __name__ == "__main__":
  from robloxpyc import pytranslator, colortext, luainit, parser, ctranslator, header #ctranslator is old and not used

  # MODULAR
  from errormanager import *
  from installationmanager import *
  from configmanager import *
  from textcompiler import *
  from basecompilers import *
  from util import *
  from plugin import *
  from loader import loader
else:
  from . import pytranslator, colortext, luainit, parser, ctranslator, header #ctranslator is old and not used

  # MODULAR
  from .errormanager import *
  from .installationmanager import *
  from .configmanager import *
  from .textcompiler import *
  from .basecompilers import *
  from .util import *
  from .plugin import *
  from .loader import loader
# BUILTIN
import subprocess,shutil,sys,threading,json,requests,traceback,pkg_resources,re,sys,webbrowser,pickle, os, zipfile


registryrawurl = "https://raw.githubusercontent.com/roblox-pyc/registry/main/registry.json"
global count
count = 0

try:
  registry = json.loads(requests.get(registryrawurl).text)
except json.JSONDecodeError:
  print(colortext.white("Import will not work, registry is corrupted. Please report this issue to the github repo, discord server, or the devforum post\nthanks!"))
  registry = {} 


# Download from wally 
def wallyget(author, name, isDependant=False):
  # Use wally and download the zip and unpack it
  print(info(f"Getting @{author}/{name} metadata", "roblox-pyc wally"))
  wallyurl = "https://api.wally.run/v1/"
  
  # first get package metadata should look like:
  metadataurl = wallyurl+"/package-metadata/"+author+"/"+name
  data = requests.get(metadataurl).text
  jsondata = json.loads(data)
  
  if 'message' in jsondata:
    print(error(jsondata["message"]))
    print(error("Exiting process", "roblox-pyc wally"))
    sys.exit()
  jsondata = json.loads(data)["versions"]
  #get latest version and dependencies
  latestver = jsondata[0]
  vernum = latestver["package"]["version"]
  dependencies = latestver["dependencies"]
  
  for i in dependencies:
    dependency = dependencies[i]
    print("Downloading dependency "+dependency+"...")
    wallyget(dependency.split("/")[0], dependency.split("/")[1].split("@")[0], True)
  
  # Download the package
  if not isDependant:
    print("\n"*2)
    print("Dependencies downloaded, now downloading package...")
    print(info(f"Downloading @{author}/{name} v{vernum}", "roblox-pyc wally"))
  url = wallyurl+"/package-contents/"+author+"/"+name+"/"+vernum
  headers = {"Wally-Version": "1.0.0"} 
  response = requests.get(url, headers=headers).content
  
  # create new file in cwd/dependencies called author_name_version.zip and unzip it
  print(info("Saving package...", "roblox-pyc wally"))
  #### if dependencies folder doesnt exist, create it
  if not os.path.exists(os.path.join(os.getcwd(), "dependencies")):
    os.makedirs(os.path.join(os.getcwd(), "dependencies"))
  ####
  open(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name+".zip"), "x").close()
  with open(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name+".zip"), "wb") as file:
    file.write(response)
  # unzip
  print(info("Unzipping package...", "roblox-pyc wally"))
  with zipfile.ZipFile(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name+".zip"), 'r') as zip_ref:
    zip_ref.extractall(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name))
  # delete the zip
  print(info("Deleting uneeded resources...", "roblox-pyc wally"))
  os.remove(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name+".zip"))

# CLI PACKAGES
# ASYNC 


# TODO: Create a template for the 
def w():
  try:
    def incli():
      # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
      path = os.getcwd()

      #global count
      #count = 0
      localcount = 0
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".py"):
            localcount += 1
      newloader = loader(localcount)
      
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".py"):
            threading.Thread(target=pycompile, args=(r, file, newloader)).start()
            #pycompile(r, file)
          else:
            othercompile(r, file)
      
      newloader.yielduntil()
      
      print(colortext.green("Compiled Files!"))
      if getconfig("general", "autocompile", False):
        action = input("")
        if action == "exit":
          exit(0)
        else:
          incli()
    
    def incli2():
      # Just like incli, but duplicates the direcotry with -compiled and compiles the files in there, also runs filtercompiledfolder() on the directory
      path = os.getcwd()+"-compiled"
      if os.path.exists(path):
        # delete the folder and child files
        shutil.rmtree(path)
      shutil.copytree(os.getcwd(), path)

      #global count
      #count = 0
      localcount = 0
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".py"):
            localcount += 1
      newloader = loader(localcount)
      
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".py"):
            threading.Thread(target=pycompile, args=(r, file, newloader)).start()
            
          else:
            othercompile(r, file)
      newloader.yielduntil()
      filtercompiledfolder()
      print(colortext.green("Compiled Files!"))
      if getconfig("general", "autocompile", False):
        action = input("")
        if action == "exit":
          exit(0)
        else:
          incli2()
    if sys.argv.__len__() >= 1:
      if sys.argv[1] == "p":
        p()
      elif sys.argv[1] == "lib":
        # sys.argv[2] is the path to the file, create a new file there with the name robloxpyc.lua, and write the library to it
        lib()
      elif sys.argv[1] == "c":
        decreapted("c")
        # Go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(warn("Are you sure? This will delete all .lua files and add a .py file with the same name.\n\nType 'yes' to continue."))
        if confirm == "yes":   
          path = os.getcwd()
          
          for r, d, f in os.walk(path):
            for file in f:
              if '.lua' in file:
                luafilecontents = ""
                with open(os.path.join(r, file), "r") as f:
                  luafilecontents = f.read()
                  
                os.remove(os.path.join(r, file))
                
                # create new file with same name but  .py and write the lua file contents to it
                open(os.path.join(r, file.replace(".lua", ".py")), "x").close()
                # write the old file contents as a py comment
                open(os.path.join(r, file.replace(".lua", ".py")), "w").write('"""\n'+luafilecontents+'\n"""')
                print(colortext.green("Converted to py "+os.path.join(r, file)+" as "+file.replace(".lua", ".py")))
      elif sys.argv[1] == "cd":
        # Duplicate the cwd directory, the original will be renamed to -compiled and the new one will be renamed to the original. For the new one, go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(warn("Are you sure? This will duplicate the current directory and compile the files in the new directory.\n\nType 'yes' to continue."))
        if confirm == "yes":
          path = os.getcwd()+"/src"
          # check if cwd/default.project.json exists, if it does, then use that as the default project file
          #if os.path.exists(os.getcwd()+"/default.project.json"):
          #  formatdefaultproj(os.getcwd()+"/default.project.json")
          # rename directory to -compiled
          os.rename(path, path+"-compiled")
          # duplicate the directory, remove the -compiled from the end
          shutil.copytree(path+"-compiled", path)
          # now we have 2 identical directories, one with -compiled and one without. for the one without, go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
          path = os.getcwd()

          for r, d, f in os.walk(backwordreplace(path, "-compiled", "", 1)):
            for file in f:
              if '.lua' in file:
                luafilecontents = ""
                with open(os.path.join(r, file), "r") as f:
                  luafilecontents = f.read()
                  
                os.remove(os.path.join(r, file))
                
                # create new file with same name but  .py and write the lua file contents to it
                open(os.path.join(r, file.replace(".lua", ".py")), "x").close()
                # write the old file contents as a C++ comment
                open(os.path.join(r, file.replace(".lua", ".py")), "w").write("\"\"\"\n"+luafilecontents+"\n\"\"\"")
                
                print(colortext.green("Converted "+os.path.join(r, file)+" to "+file.replace(".lua", ".py")))
          # create a .rpyc file in the non -compiled directory
          open(os.path.join(backwordreplace(path, "-compiled", "", 1), ".rpyc"), "x").close()
          # set cwd to not -compiled
          os.chdir(backwordreplace(path, "-compiled", "", 1))
          print(info("Completed! You may need to modify the default.package.json or any other equivalent file to make it use the -compiled directory rather than the original."))
      elif sys.argv[1] == "w":
        print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
      elif sys.argv[1] == "d":
        print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli2()
      
  except IndexError:
    print(error("Invalid amount of arguments!", "roblox-py"))
  except KeyboardInterrupt:
    print(colortext.red("Aborted!"))
    sys.exit(0)
def cw():
  try:
    print(warn("Note, this is not yet completed and will not work and is just a demo to show the AST and very light nodevisitor. A production version will be released soon."))
    def incli():
      #global count
      #count = 0
      localcount = 0
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".c"):
            localcount += 1
      newloader = loader(localcount)
      path = os.getcwd()

      for r, d, f in os.walk(path):
        for file in f:
            # check if it ENDS with .c, not if it CONTAINS .c
            # Run use threading 
          if file.endswith(".c"):
            localcount += 1
            threading.Thread(target=ccompile, args=(r, file, newloader)).start()
            #ccompile(r, file)
          else:
            othercompile(r, file)
      newloader.yielduntil()
      print(colortext.green("Compiled Files!"))
      if getconfig("general", "autocompile", False):
        action = input("")
        if action == "exit":
          exit(0)
        else:
          incli()
    def incli2():
      # Just like incli, but duplicates the direcotry with -compiled and compiles the files in there, also runs filtercompiledfolder() on the directory
      path = os.getcwd()+"-compiled"
      if os.path.exists(path):
        # delete the folder and child files
        shutil.rmtree(path)
      shutil.copytree(os.getcwd(), path)

      #global count
      #count = 0
      localcount = 0
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".c"):
            localcount += 1
      newloader = loader(localcount)
      
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".c"):
            threading.Thread(target=ccompile, args=(r, file, newloader)).start()
          else:
            othercompile(r, file)
      newloader.yielduntil()
      filtercompiledfolder()
      print(colortext.green("Compiled Files!"))
      if getconfig("general", "autocompile", False):
        action = input("")
        if action == "exit":
          exit(0)
        else:
          incli2()
        
        
    if sys.argv.__len__() >= 1:
      if sys.argv[1] == "p":
        print(error("Plugins are only supported for python!"))
      elif sys.argv[1] == "lib":
        # sys.argv[2] is the path to the file, create a new file there with the name robloxpyc.lua, and write the library to it
        lib()
      elif sys.argv[1] == "c":
        decreapted("c")
        # Go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(warn("Are you sure? This will delete all .lua files and add a .c file with the same name.\n\nType 'yes' to continue."))
        if confirm == "yes":   
          path = os.getcwd()
          
          for r, d, f in os.walk(path):
            for file in f:
              if '.lua' in file:
                luafilecontents = ""
                with open(os.path.join(r, file), "r") as f:
                  luafilecontents = f.read()
                  
                os.remove(os.path.join(r, file))
                
                # create new file with same name but  .py and write the lua file contents to it
                open(os.path.join(r, file.replace(".lua", ".c")), "x").close()
                # write the old file contents as a C comment
                open(os.path.join(r, file.replace(".lua", ".c")), "w").write("/*\n"+luafilecontents+"\n*/")
                print(colortext.green("Converted to c "+os.path.join(r, file)+" as "+file.replace(".lua", ".c")))
      elif sys.argv[1] == "cd":
        # Duplicate the cwd directory, the original will be renamed to -compiled and the new one will be renamed to the original. For the new one, go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(warn("Are you sure? This will duplicate the current directory and compile the files in the new directory.\n\nType 'yes' to continue."))
        if confirm == "yes":
          path = os.getcwd()+"/src"
          # rename directory to -compiled
          os.rename(path, path+"-compiled")
          # duplicate the directory, remove the -compiled from the end
          shutil.copytree(path+"-compiled", path)
          # now we have 2 identical directories, one with -compiled and one without. for the one without, go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
          path = os.getcwd()

          for r, d, f in os.walk(backwordreplace(path, "-compiled", "", 1)):
            for file in f:
              if '.lua' in file:
                luafilecontents = ""
                with open(os.path.join(r, file), "r") as f:
                  luafilecontents = f.read()
                  
                os.remove(os.path.join(r, file))
                
                # create new file with same name but  .py and write the lua file contents to it
                open(os.path.join(r, file.replace(".lua", ".c")), "x").close()
                # write the old file contents as a C++ comment
                open(os.path.join(r, file.replace(".lua", ".c")), "w").write("/*\n"+luafilecontents+"\n*/")
                
                print(colortext.green("Converted "+os.path.join(r, file)+" to "+file.replace(".lua", ".c")))
          open(os.path.join(backwordreplace(path, "-compiled", "", 1), ".rpyc"), "x").close()
          # set cwd to not -compiled
          os.chdir(backwordreplace(path, "-compiled", "", 1))
          print(info("Completed! You may need to modify the default.package.json or any other equivalent file to make it use the -compiled directory rather than the original."))
      elif sys.argv[1] == "w":
        print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
      elif sys.argv[1] == "d":
        print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli2()
      
  except IndexError:
    print(error("Invalid amount of arguments!", "roblox-c"))
  except KeyboardInterrupt:
    print(colortext.red("Aborted!"))
    sys.exit(0)
def cpw():
  
  try:
    print(warn("Note, this is not yet completed and will not work and is just a demo to show the AST and very light nodevisitor. A production version will be released soon."))
    def incli():
      # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
      path = os.getcwd()
      #global count
      #count = 0
      localcount = 0
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".cpp"):
            localcount += 1
      newloader = loader(localcount)
      for r, d, f in os.walk(path):
        for file in f:
            if file.endswith(".cpp"):
              # compile the file to a file with the same name and path but .lua
              threading.Thread(target=cppcompile, args=(r, file, newloader)).start()
              #cppcompile(r, file)
            else:
              othercompile(r, file)
      newloader.yielduntil()
      print(colortext.green("Compiled Files!"))
      
      if getconfig("general", "autocompile", False):
        action = input("")
        if action == "exit":
          exit(0)
        else:
          incli()
    def incli2():
      # Just like incli, but duplicates the direcotry with -compiled and compiles the files in there, also runs filtercompiledfolder() on the directory
      path = os.getcwd()+"-compiled"
      if os.path.exists(path):
        # delete the folder and child files
        shutil.rmtree(path)
      shutil.copytree(os.getcwd(), path)

      #global count
      #count = 0
      localcount = 0
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".cpp"):
            localcount += 1
      newloader = loader(localcount)
      
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".cpp"):
            threading.Thread(target=cppcompile, args=(r, file, newloader)).start()
          else:
            othercompile(r, file)
      newloader.yielduntil()
      filtercompiledfolder()
      print(colortext.green("Compiled Files!"))
      if getconfig("general", "autocompile", False):
        action = input("")
        if action == "exit":
          exit(0)
        else:
          incli2()
          
      
    if sys.argv.__len__() >= 1:
      if sys.argv[1] == "p":
        print(error("Plugins are only supported for python!"))
      elif sys.argv[1] == "lib":
        # sys.argv[2] is the path to the file, create a new file there with the name robloxpyc.lua, and write the library to it
        lib()
      elif sys.argv[1] == "c":
        decreapted("c")
        # Go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(warn("Are you sure? This will delete all .lua files and add a .cpp file with the same name.\n\nType 'yes' to continue."))
        if confirm == "yes":   
          path = os.getcwd()
          
          for r, d, f in os.walk(path):
            for file in f:
              if '.lua' in file:
                luafilecontents = ""
                with open(os.path.join(r, file), "r") as f:
                  luafilecontents = f.read()
                  
                os.remove(os.path.join(r, file))
                
                # create new file with same name but  .py and write the lua file contents to it
                open(os.path.join(r, file.replace(".lua", ".cpp")), "x").close()
                # write the old file contents as a C++ comment
                open(os.path.join(r, file.replace(".lua", ".cpp")), "w").write("/*\n"+luafilecontents+"\n*/")
                
                print(colortext.green("Converted to c++ "+os.path.join(r, file)+" as "+file.replace(".lua", ".cpp")))
      elif sys.argv[1] == "cd":
        # Duplicate the cwd directory, the original will be renamed to -compiled and the new one will be renamed to the original. For the new one, go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(warn("Are you sure? This will duplicate the current directory and compile the files in the new directory.\n\nType 'yes' to continue."))
        if confirm == "yes":
          path = os.getcwd()+"/src"
          # rename directory to -compiled
          os.rename(path, path+"-compiled")
          # duplicate the directory, remove the -compiled from the end
          shutil.copytree(path+"-compiled", path)
          # now we have 2 identical directories, one with -compiled and one without. for the one without, go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
          path = os.getcwd()

          for r, d, f in os.walk(backwordreplace(path, "-compiled", "", 1)):
            for file in f:
              if '.lua' in file:
                luafilecontents = ""
                with open(os.path.join(r, file), "r") as f:
                  luafilecontents = f.read()
                  
                os.remove(os.path.join(r, file))
                
                # create new file with same name but  .py and write the lua file contents to it
                open(os.path.join(r, file.replace(".lua", ".cpp")), "x").close()
                # write the old file contents as a C++ comment
                open(os.path.join(r, file.replace(".lua", ".cpp")), "w").write("/*\n"+luafilecontents+"\n*/")
                
                print(colortext.green("Converted "+os.path.join(r, file)+" to "+file.replace(".lua", ".cpp")))
          open(os.path.join(backwordreplace(path, "-compiled", "", 1), ".rpyc"), "x").close()
          # set cwd to not -compiled
          os.chdir(backwordreplace(path, "-compiled", "", 1))
          print(info("Completed! You may need to modify the default.package.json or any other equivalent file to make it use the -compiled directory rather than the original."))
      elif sys.argv[1] == "w":
        print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
      elif sys.argv[1] == "d":
        print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli2()
      
  except IndexError:
    print(error("Invalid amount of arguments!", "roblox-cpp"))
  except KeyboardInterrupt:
    print(colortext.red("Aborted!"))   
    sys.exit(0)
def lunar():
  try:
    checkboth() # install luarocks and moonscript if not installed
    def incli():
      # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
      path = os.getcwd()
      #global count
      #count = 0
      localcount = 0
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".moon"):
            localcount += 1
      newloader = loader(localcount)
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".moon"):
            localcount += 1
            threading.Thread(target=lunarcompile, args=(r, file, newloader)).start()
            #lunarcompile(r, file)
          else:
            othercompile(r, file)
      newloader.yielduntil()  
      print(colortext.green("Compiled Files!"))
      if getconfig("general", "autocompile", False):
        action = input("")
        if action == "exit":
          exit(0)
        else:
          incli()
    def incli2():
      # Just like incli, but duplicates the direcotry with -compiled and compiles the files in there, also runs filtercompiledfolder() on the directory
      path = os.getcwd()+"-compiled"
      if os.path.exists(path):
        # delete the folder and child files
        shutil.rmtree(path)
      shutil.copytree(os.getcwd(), path)

      #global count
      #count = 0
      localcount = 0
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".moon"):
            localcount += 1
      newloader = loader(localcount)
      
      for r, d, f in os.walk(path):
        for file in f:
          if file.endswith(".moon"):
            threading.Thread(target=lunarcompile, args=(r, file, newloader)).start()
          else:
            othercompile(r, file)
      newloader.yielduntil()
      filtercompiledfolder()
      print(colortext.green("Compiled Files!"))
      if getconfig("general", "autocompile", False):
        action = input("")
        if action == "exit":
          exit(0)
        else:
          incli2()
    if sys.argv.__len__() >= 1:
      if sys.argv[1] == "p":
        print(error("Plugins are only supported for python!"))
      elif sys.argv[1] == "lib":
        # sys.argv[2] is the path to the file, create a new file there with the name robloxpyc.lua, and write the library to it
        lib()
      elif sys.argv[1] == "c":
        decreapted("c")
        # Go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(warn("Are you sure? This will delete all .lua files and add a .moon file with the same name.\n\nType 'yes' to continue."))
        if confirm == "yes":   
          path = os.getcwd()
          
          for r, d, f in os.walk(path):
            for file in f:
              if '.lua' in file:
                luafilecontents = ""
                with open(os.path.join(r, file), "r") as f:
                  luafilecontents = f.read()
                  
                os.remove(os.path.join(r, file))
                
                # create new file with same name but  .py and write the lua file contents to it
                open(os.path.join(r, file.replace(".lua", ".moon")), "x").close()
                # write the old file contents as a C++ comment
                open(os.path.join(r, file.replace(".lua", ".moon")), "w").write("--[[\n"+luafilecontents+"\n]]")
                
                print(colortext.green("Converted to lunar "+os.path.join(r, file)+" as "+file.replace(".lua", ".moon")))
      elif sys.argv[1] == "w":
        print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
      elif sys.argv[1] == "cd":
        # Duplicate the cwd directory, the original will be renamed to -compiled and the new one will be renamed to the original. For the new one, go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(warn("Are you sure? This will duplicate the current directory and compile the files in the new directory.\n\nType 'yes' to continue."))
        if confirm == "yes":
          path = os.getcwd()+"/src"
          # rename directory to -compiled
          os.rename(path, path+"-compiled")
          # duplicate the directory, remove the -compiled from the end
          shutil.copytree(path+"-compiled", path)
          # now we have 2 identical directories, one with -compiled and one without. for the one without, go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
          path = os.getcwd()

          for r, d, f in os.walk(backwordreplace(path, "-compiled", "", 1)):
            for file in f:
              if '.lua' in file:
                luafilecontents = ""
                with open(os.path.join(r, file), "r") as f:
                  luafilecontents = f.read()
                  
                os.remove(os.path.join(r, file))
                
                # create new file with same name but  .py and write the lua file contents to it
                open(os.path.join(r, file.replace(".lua", ".moon")), "x").close()
                # write the old file contents as a C++ comment
                open(os.path.join(r, file.replace(".lua", ".moon")), "w").write("--[[\n"+luafilecontents+"\n]]")
                
                print(colortext.green("Converted "+os.path.join(r, file)+" to "+file.replace(".lua", ".moon")))
          open(os.path.join(backwordreplace(path, "-compiled", "", 1), ".rpyc"), "x").close()
          # set cwd to not -compiled
          os.chdir(backwordreplace(path, "-compiled", "", 1))
          print(info("Completed! You may need to modify the default.package.json or any other equivalent file to make it use the -compiled directory rather than the original."))
      elif sys.argv[1] == "d":
        print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli2()
      
  except IndexError:
    print(error("Invalid amount of arguments!", "roblox-lunar"))
  except KeyboardInterrupt:
    print(colortext.red("Aborted!"))     
    sys.exit(0)  
def globalincli():
  # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
  path = os.getcwd()
  #global count
  #count = 0
  localcount = 0
  for r, d, f in os.walk(path):
    for file in f:
      if file.endswith(".moon") or file.endswith(".py") or file.endswith(".ts") or file.endswith(".tsx"): #or file.endswith(".c") or file.endswith(".cpp"):
        localcount += 1
  newloader = loader(localcount)
  for r, d, f in os.walk(path):
    for file in f:
      if file.endswith(".moon"):
        localcount += 1
        threading.Thread(target=lunarcompile, args=(r, file, newloader)).start()
        #lunarcompile(r, file)
      elif file.endswith(".py"):
        localcount += 1
        threading.Thread(target=pycompile, args=(r, file, newloader)).start()
      elif file.endswith(".ts") or file.endswith(".tsx"):
        threading.Thread(target=robloxtscompile, args=(r, file, newloader)).start()
      else:
        othercompile(r, file)
  newloader.yielduntil()  
  print(colortext.green("Compiled Files!"))
  action = input("")
  if action == "exit":
    exit(0)
  else:
    globalincli()
def globalincli2():
  # Just like incli, but duplicates the direcotry with -compiled and compiles the files in there, also runs filtercompiledfolder() on the directory
  path = os.getcwd()+"-compiled"
  if os.path.exists(path):
    # delete the folder and child files
    shutil.rmtree(path)
  shutil.copytree(os.getcwd(), path)

  #global count
  #count = 0
  localcount = 0
  for r, d, f in os.walk(path):
    for file in f:
      if file.endswith(".moon") or file.endswith(".py") or file.endswith(".ts") or file.endswith(".tsx"): #or file.endswith(".c") or file.endswith(".cpp"):
        localcount += 1
  newloader = loader(localcount)
      
  for r, d, f in os.walk(path):
    for file in f:
      if file.endswith(".moon"):
        threading.Thread(target=lunarcompile, args=(r, file, newloader)).start()
      elif file.endswith(".py"):
        localcount += 1
        threading.Thread(target=pycompile, args=(r, file, newloader)).start()
      elif file.endswith(".ts") or file.endswith(".tsx"):
        threading.Thread(target=robloxtscompile, args=(r, file, newloader)).start()
      else:
        othercompile(r, file)
  newloader.yielduntil()
  filtercompiledfolder()
  print(colortext.green("Compiled Files!"))
  action = input("")
  if action == "exit":
    exit(0)
  else:
    globalincli2()
def pyc():
  title = colortext.magenta("roblox-pyc", ["bold"])
  py = colortext.blue("roblox-py", ["bold"])
  c = colortext.blue("roblox-c", ["bold"])
  cpp = colortext.blue("roblox-cpp", ["bold"])
  lunar = colortext.blue("roblox-lunar", ["bold"])
  border = colortext.white("--------------------")
  blank = colortext.blue("roblox-", ["bold"])+colortext.magenta("<lang>")
  blank2 = colortext.blue("rblx-", ["bold"])+colortext.magenta("<lang>")
  blankpath = colortext.magenta("<path>")
  selftool = colortext.blue("roblox-pyc", ["bold"])
  shortselftool = colortext.blue("rblx-pyc", ["bold"])
  shorterselftool = colortext.blue("rpyc", ["bold"])
  try:
    if sys.argv[1] == "config":
      # Open config menu
      print(f"""
Config menu
{border} 
1 - {py}
2 - {c}
3 - {cpp}
4 - {lunar}   
5 - General      
      """)
      returnval = input("Select which config to open: ")
      
      if returnval == "1":
        print(f"{py} doesnt need to be configured!")
      elif returnval == "2":
        print(f"""
Configuring {c}
{border}
1 - Change std 
2 - Change stdlib
              """)
        
        inputval = input("Select which config to open: ")
        if inputval == "1":
          returned = input("Enter the std, it currently is %s: " % getconfig("c", "std", "c11"))
          setconfig("c", "std", returned, "c11")
        elif inputval == "2":
          returned = input("Enter the stdlib, it currently is %s: " % getconfig("c", "stdlib", "libc"))
          setconfig("c", "stdlib", returned, "libc")
      elif returnval == "3": #
        print(f"""
Configuring {cpp}
{border}
1 - Change std 
2 - Change stdlib
              """)
        
        inputval = input("Select which config to open: ")
        if inputval == "1":
          returned = input("Enter the std, it currently is %s: " % getconfig("cpp", "std", "c++11"))
          setconfig("cpp", "std", returned, "c++11")
        elif inputval == "2":
          returned = input("Enter the stdlib, it currently is %s: " % getconfig("cpp", "stdlib", "libc++"))
          setconfig("cpp", "stdlib", returned, "libc++")
      elif returnval == "4":
        print(f"{lunar} doesnt need to be configured!")
      elif returnval == "5":
        print(f"""
Configuring General Settings
{border}
1 - Change C and C++ dylib
2 - Change LLVM Home Path (only for C and C++)
3 - Change LD-LIBRARY-PATH (only for C and C++)
4 - Enable or diable autocompile
              """)
        inputval = input("Select which config to open: ")
        if inputval == "1":
          returned = input("Enter the dynamic library file, it currently is %s: " % getconfig("c", "dynamiclibpath", "None"))
          setconfig("c", "dynamiclibpath", returned, "None")
        elif inputval == "2":
          returned = input("Enter the LLVM Home Path, it currently is %s: " % getconfig("general", "llvmhomepath", "None"))
          setconfig("general", "llvmhomepath", returned, "")
          config_llvm(getconfig("general", "llvmhomepath", ""))
        elif inputval == "3":
          returned = input("Enter the LD-LIBRARY-PATH, it currently is %s: " % getconfig("general", "ldlibrarypath", "None"))
          setconfig("general", "ldlibrarypath", returned, "")
          config_llvm(None, getconfig("general", "ldlibrarypath", ""))
        elif inputval == "4":
          returned = input("Would you like to turn autocompile (on/off)")
          if returned == "on":
            setconfig("general", "autocompile", True, False)
          elif returned == "off": 
            setconfig("general", "autocompile", False, False)
          else:
            print(error("not a valid option!"))
      elif returnval == "6":
        colortext.nil(colortext.rainbow_text("Welcome to the secret menu!"))
        print("This contains many developer options and some goofy ones too!")
        print(f"""       
              1 - Traceback on error (Reccomended off, for roblox-pyc developers)
              2 - TTS on error (macOS only)
              """)
        print(f"Select which", end=" ")
        colortext.rainbow_text("secret", end=" ")
        inputval = input("config to open: ")
        if inputval == "1":
          returned = input("Click enter to confirm, CTRL+C to cancel: ")
          setconfig("general", "traceback", returned, None)
        elif inputval == "2":
          if not sys.platform == "darwin":
            print(error("I ALREADY TOLD YOU, THIS IS MACOS ONLY!"))
            return
          setconfig("general", "goofy", returned, None)
        elif inputval == "3":
          colortext.nil(colortext.rainbow_text("Welcome to the secret secret menu, sadly this is empty for now! :("))
        else:
          print(error("Aw man, you didnt select a valid option!"))
      else:
        print(error("Invalid option!"))
    elif sys.argv[1] == "devforum":
      webbrowser.open("https://devforum.com")
    elif sys.argv[1] == "discord":
      webbrowser.open("https://discord.gg/RAXYEjj3")
    elif sys.argv[1] == "github":
      webbrowser.open("https://github.com/AsynchronousAI/roblox-pyc")
    elif sys.argv[1] == "help":
      raise IndexError
    elif sys.argv[1] == "w":
      print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
      globalincli()
    elif sys.argv[1] == "d" or sys.argv[1] == ".":
      print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
      globalincli2()
    elif sys.argv[1] == "format":
      print(warn("Are you sure, this will reformat the compiled directory and delete uncompatible files, this is for when a bug occured.", "roblox-pyc"))
      if input("Type 'yes' to continue: ") == "yes":
        # Delete all files that arent .py, .moon, .lua, .c, .cpp
        filtercompiledfolder()
        print(colortext.green("Deleted all uncompatible files!"))
    elif sys.argv[1] == "p":
      print(error("Plugins are only supported for python!", "roblox-pyc"))
    elif sys.argv[1] == "lib":
      # sys.argv[2] is the path to the file, create a new file there with the name robloxpyc.lua, and write the library to it
        lib()
    elif sys.argv[1] == "c":
      decreapted("c")
      print(error("Cannot replace all files for a general language, please specify a language by using rbxpy, rbxlun, rbxc, rbxcpp", "roblox-pyc"))
    elif sys.argv[1] == "cd":
      print(error("Cannot replace all files for a general language, please specify a language by using rbxpy, rbxlun, rbxc, rbxcpp", "roblox-pyc"))
    elif sys.argv[1] == "tsc":
      # Pretty much c but for typescript and works
      if not check_roblox_ts():
        if not check_npms():
          install_npms()
        install_roblox_ts()
      confirm = input(warn("Are you sure? This will delete all .lua files and add a .ts file with the same name.\n\nType 'yes' to continue."))
      if confirm == "yes":   
        path = os.getcwd()+"/src"
        
        for r, d, f in os.walk(path):
           for file in f:
              if '.lua' in file:
                luafilecontents = ""
                with open(os.path.join(r, file), "r") as f:
                  luafilecontents = f.read()
                  
                os.remove(os.path.join(r, file))
                  
                # create new file with same name but  .py and write the lua file contents to it
                open(os.path.join(r, file.replace(".lua", ".ts")), "x").close()
                # write the old file contents as a C++ comment
                open(os.path.join(r, file.replace(".lua", ".ts")), "w").write("/*\n"+luafilecontents+"\n*/")
                  
                print(colortext.green("Converted to typescript "+os.path.join(r, file)+" as "+file.replace(".lua", ".moon")))
    elif sys.argv[1] == "info":
      subprocess.call(["pip", "show", "roblox-pyc"])
      check_for_updates()
    elif sys.argv[1] == "install":
      # Check registry for package
      if sys.argv[2] in registry:
        # Find out how to install, cli or package
        item = registry[sys.argv[2]]
        type = item["type"]
        
        if type == "cli":
          if True:
            print(error("CLI packages are not supported on this build!", "roblox-pyc"))
            return
          # git clone the files to this scripts path
          print(colortext.green("Installing "+sys.argv[2]+" ..."))
          selfpath = os.path.dirname(os.path.realpath(__file__))
          # create new dir in selfpath called sys.argv[2]
          os.mkdir(os.path.join(selfpath, sys.argv[2]))
          
          subprocess.call(["git", "clone", item["url"], os.path.join(selfpath, sys.argv[2])])
          
          # add to config
          newlist = getconfig("general", "cli", [])
          newlist.append({"name": sys.argv[2], "path": os.path.join(selfpath, sys.argv[2]), "mainscript": item["mainscript"], "target": item["target"], "command": item["command"]})  
        elif type == "luaext":
          # save to config the name and url data after request
          print(colortext.green("Fetching "+sys.argv[2]+" ..."))
          newlist = getconfig("general", "luaext", [])
          packagedata = json.loads(requests.get(item["url"]).text)
          fileurl = packagedata["file"]
          
          newlist.append({"name": sys.argv[2], "data": requests.get(fileurl).text, "var": packagedata["outputvar"]})
          setconfig("general", "luaext", newlist, [])
          print(colortext.green("Fetched "+sys.argv[2]+"!"))
        elif type == "package":
          # Create new folder in cwd called dependencies if it doesnt exist
          print(colortext.green("Installing "+sys.argv[2]+" ..."))
          exists = os.path.exists(os.path.join(os.getcwd(), "dependencies"))
          if not exists:
            lib()
          
          # Gitclone item["url"] to dependencies folder
          subprocess.call(["git", "clone", item["url"], os.path.join(os.getcwd(), "dependencies", sys.argv[2])])
          print(colortext.green("Installed "+sys.argv[2]+"!"))
      elif sys.argv[2].startswith("@") and not sys.argv[2].startswith("@rbxts"):
        author = sys.argv[2].split("/")[0].replace("@", "")
        name = sys.argv[2].split("/")[1]
        wallyget(author, name)
      elif sys.argv[2].startswith("@rbxts"):
        # Use NPM
        print(warn("Fetching from NPM is still not stable, you might get missing files or files in the wrong place."))
        if not check_npms():
          install_npms()
        # Install to /dependencies not /node_modules
        subprocess.call(["npm", "install", sys.argv[2], "--prefix=dependencies"])
        # Delete dependencies/package-lock.json and dependencies/package.json. Use try except
        try:
          os.remove(os.path.join(os.getcwd(), "dependencies", "package-lock.json"))
        except:
          pass
        try:
          os.remove(os.path.join(os.getcwd(), "dependencies", "package.json"))
        except:
          pass
        try:
          os.remove(os.path.join(os.getcwd(), "dependencies", ".package.json"))
        except:
          pass
        try:
          os.remove(os.path.join(os.getcwd(), "dependencies", ".package-lock.json"))
        except:
          pass
        
        # Unpack dependencies/node_modules to dependencies
        for r, d, f in os.walk(os.path.join(os.getcwd(), "dependencies", "node_modules")):
          for file in f:
            shutil.move(os.path.join(r, file), os.path.join(os.getcwd(), "dependencies"))
        # Delete dependencies/node_modules
        shutil.rmtree(os.path.join(os.getcwd(), "dependencies", "node_modules"))
        # If a dependency/.package.json exists or a dependency/.package-lock.json exists, delete it
        try:
          os.remove(os.path.join(os.getcwd(), "dependencies", ".package.json"))
        except:
          pass
        try:
          os.remove(os.path.join(os.getcwd(), "dependencies", ".package-lock.json"))
        except:
          pass
        try:
          os.remove(os.path.join(os.getcwd(), "dependencies", "package-lock.json"))
        except:
          pass
        try:
          os.remove(os.path.join(os.getcwd(), "dependencies", "package.json"))
        except:
          pass
          
        
      else:
        print(warn("roblox-pyc: Package not in registry!")+"\n\n"+info("If you are trying to install from Wally enter the package name as @<scope>/<package>")+"\n\n"+info("If you are trying to install from roblox-ts enter the package name as @rbxts/<package>")+"\nInstall from one of these other package managers:")
        print("""
    1 - luarocks
    2 - pip (compiles to lua)
    3 - pip3 (compiles to lua)
    5 - None
              """)
        returnval = input("Select which package manager to use: ")
        if returnval == "1":
          # install to dependencies folder
          if not check_luarocks():
            install_luarocks()
          subprocess.call(["luarocks", "install", sys.argv[2], "--tree=dependencies"])
        elif returnval == "2":
          # install to dependencies folder
          subprocess.call(["pip", "install", sys.argv[2], "--target=dependencies", "--upgrade"])
          # compile the newly added directory to lua
        elif returnval == "3":
          # install to dependencies folder
          subprocess.call(["pip3", "install", sys.argv[2], "--target=dependencies", "--upgrade"])
          # compile the newly added directory to lua  
        else:
          print("Invalid option or exited.")
          return
        print("Compiling to luau...")
        #global count
        #count = 0
        endcount = 0
        for r, d, f in os.walk(os.path.join(os.getcwd(), "dependencies")):
          for file in f:
              if file.endswith(".py") or file.endswith(".moon"):
                endcount+=1
        newloader = loader(endcount)
        for r, d, f in os.walk(os.path.join(os.getcwd(), "dependencies")):
          # if dir name is __pycache__ delete it
          if os.path.basename(r) == "__pycache__":
            # clear children
            for child in os.listdir(r):
              try:
                os.remove(os.path.join(r, child))
              except:
                pass
            try:
              os.rmdir(r)
            except:
              pass      
    
          for file in f:
            if file.endswith(".py"):
              endcount+=1
              threading.Thread(target=pycompile, args=(r, file, newloader)).start()
              
              # delete old file
              os.remove(os.path.join(r, file))
            elif file.endswith(".moon"):
              endcount+=1
              threading.Thread(target=lunarcompile, args=(r, file, newloader)).start()
                
              # delete old file
              os.remove(os.path.join(r, file))
            elif file.endswith(".c") or file.endswith(".cpp"):
              candcpperror()
            else:
              othercompile(r, file)
              
        
        
        newloader.yielduntil()
        print("Successfully installed "+sys.argv[2]+"!")
        print(warn("Since these modules are from 3rd party sources, they may not work in the roblox environment and you may encounter errors, this is feauture is experimental and any issues in your code caused by this is not our fault."))
        
    elif sys.argv[1] == "uninstall":
      # Find out how to install, cli or package
        item = registry[sys.argv[2]]
        type = item["type"]
        
        # for cli do nothing, for luaext remove from config, for package remove from dependencies folder
        if type == "cli":
          pass
        elif type == "luaext":
          currentlist = getconfig("general", "luaext", [])
          # remove, if not found error
          found = False
          
          for i in currentlist:
            if i["name"] == sys.argv[2]:
              currentlist.remove(i)
              found = True
          if not found:
            print(error("Module not found!", "roblox-pyc"))
          else:
            setconfig("general", "luaext", currentlist, [])
            print(colortext.green("Uninstalled "+sys.argv[2]+"!"))
        elif type == "package":
          dependenciesPath = os.path.join(os.getcwd(), "dependencies")
          # if it doesnt exist error
          if not os.path.exists(dependenciesPath):
            print(error("Dependencies folder not found! Creating one now...", "roblox-py"))
            lib()
            return
          # remove, if not found error
          if not os.path.exists(os.path.join(dependenciesPath, sys.argv[2])):
            print(error("Package not found!", "roblox-py"))
          
          if os.path.exists(os.path.join(dependenciesPath, sys.argv[2])):
            shutil.rmtree(os.path.join(dependenciesPath, sys.argv[2]))
            print(colortext.green("roblox-pyc: Uninstalled "+sys.argv[2]+"!"))
    elif sys.argv[1] == "list":
      # First list all items in config
      print(colortext.green("Extensions:"))
      for i in getconfig("general", "luaext", []):
        print(("  - "+i["name"]))
      
      print(colortext.green("Packages:"))
      # Then list all items in dependencies folder
      dependenciesPath = os.path.join(os.getcwd(), "dependencies") 
      if not os.path.exists(dependenciesPath):
        print(warn("roblox-pyc: Dependencies folder not found! Creating one now..."))
        lib()
        return
      for i in os.listdir(dependenciesPath):
        print(("  - "+i))
    else:
      raise IndexError
  except IndexError:
    print(f"""
{title}
{border}
  CLIs:
  - {py} - Python to Lua | Best for a functional and simple language
  - {c} - C to Lua | Best for learning a more complicated language for fun and educational purposes
  - {cpp} - C++ to Lua | Best for learning a more complicated OOP language for fun and educational purposes
  - {lunar} - Lunar to Lua | Best for learning a language with some great syntax sugar
  {border}
  NOTES:
  - {py} is the only one that supports plugins, and it supports full python 3.13, which is a dev build of python
  - {c} and {cpp} are only capable of light conversions, and are not capable of converting complex code at the time of writing.
  - {lunar} is based off MoonScript, and is completed and reccomended if you want a really nice language with good syntax sugar.
  - I would highly reccomend {py} and {lunar} for production use over ideal lua, as they are much more powerful and easier to use.
  - At the moment lunar is the exact same as moonscript, but adding roblox specific features is planned.
  - rpyc and rblx-pyc can be used rather than roblox-pyc, they are just shorter versions of the name.
  {border}
  CLI DOCS:
  - {blank} w - Click enter in the terminal to compile all scripts
  - {blank} p - Start the plugin server (only for {py})
  - {blank} lib - Generate dependencies folder with stdlib
  - {blank} c - Convert all .lua files to targeted language files, it will comment the existing lua code
  - {blank2} w - Click enter in the terminal to compile all scripts
  - {blank2} p - Start the plugin server (only for {py})
  - {blank2} lib - Generate dependencies folder with stdlib
  - {blank2} c - Convert all .lua files to targeted language files, it will comment the existing lua code
  - {selftool} config - Open the config menu
  - {selftool} devforum - Open the devforum page in a browser
  - {selftool} discord - Open the discord server in a browser
  - {selftool} github - Open the github page in a browser
  - {selftool} install <package> - Install a item from the registry. Read docs for more info
  - {selftool} uninstall <package> - Uninstall a item from the registry. Read docs for more info
  - {selftool} list - List all installed packages
  {border}
  MORE HELP:
  - Devforum
  - Discord
  - Github Issues

          """)
  except KeyboardInterrupt:
    print(colortext.red("Aborted!"))  
    sys.exit(0)
  

if __name__ == "__main__":
  print(colortext.blue("Test mode"))
  mode = input("Select which module to run (1, 2, 3, 4): ")
  
  if mode == "1":
    w()
  elif mode == "2":
    cw()
  elif mode == "3":
    cpw()
  elif mode == "4":
    lunar()
  else:
    pyc()