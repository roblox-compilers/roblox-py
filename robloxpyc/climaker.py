# TODO

import sys

if not (os.path.dirname(os.path.abspath(__file__)).startswith(sys.path[-1])):
    from loader import loader
    from textcompiler import *
    from configmanager import *
    from util import *
    from basecompilers import *
else:
    from .loader import loader
    from .textcompiler import *
    from .configmanager import *
    from .util import *
    from .basecompilers import *
import threading, shutil
    

def newLanguage(file, func, commentart):
    pass
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