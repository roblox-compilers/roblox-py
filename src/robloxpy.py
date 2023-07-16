import os
from flask import Flask, request
from pyflakes import api
import re
import sys
import webbrowser
import pickle
from . import pytranslator, colortext, luainit, parser, ctranslator, luainit, header #ctranslator is old and not used
import subprocess
import shutil
import sys

class Reporter:
    """
    Formats the results of pyflakes checks to users.
    """
    def __init__(self):
        self.diagnostics = []

    def unexpectedError(self, filename, msg):
        """
        An unexpected error occurred trying to process C{filename}.

        @param filename: The path to a file that we could not process.
        @ptype filename: C{unicode}
        @param msg: A message explaining the problem.
        @ptype msg: C{unicode}
        """
        self.diagnostics.append(f"1{filename}: {msg}\n")

    def syntaxError(self, filename, msg, lineno, offset, text):
        """
        There was a syntax error in C{filename}.

        @param filename: The path to the file with the syntax error.
        @ptype filename: C{unicode}
        @param msg: An explanation of the syntax error.
        @ptype msg: C{unicode}
        @param lineno: The line number where the syntax error occurred.
        @ptype lineno: C{int}
        @param offset: The column on which the syntax error occurred, or None.
        @ptype offset: C{int}
        @param text: The source code containing the syntax error.
        @ptype text: C{unicode}
        """
        if text is None:
            line = None
        else:
            line = text.splitlines()[-1]

        # lineno might be None if the error was during tokenization
        # lineno might be 0 if the error came from stdin
        lineno = max(lineno or 0, 1)

        if offset is not None:
            # some versions of python emit an offset of -1 for certain encoding errors
            offset = max(offset, 1)
            self.diagnostics.append('1%s:%d:%d: %s\n' %
                               (filename, lineno, offset, msg))
        else:
            self.diagnostics.append('1%s:%d: %s\n' % (filename, lineno, msg))

        if line is not None:
            self.diagnostics.append(line)
            self.diagnostics.append('\n')
            if offset is not None:
                self.diagnostics.append(re.sub(r'\S', ' ', line[:offset - 1]) +
                                   "^\n")

    def flake(self, message):
        """
        pyflakes found something wrong with the code.

        @param: A L{pyflakes.messages.Message}.
        """
        self.diagnostics.append("2"+str(message))
        self.diagnostics.append('\n')


app = Flask(__name__)
translator = pytranslator.Translator()

# INSTALL MOONSCRIPT
def check_luarocks():
    try:
        subprocess.call(["luarocks", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def check_moonscript():
    try:
        subprocess.call(["moonc", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False
      
def install_luarocks():
    print("Installing LuaRocks...")
    subprocess.call(["apt-get", "install", "-y", "luarocks"])

def install_moonscript():
    print("Installing MoonScript...")
    subprocess.call(["luarocks", "install", "moonscript", "--dev"])

def checkboth():
    if check_luarocks() == False:
        print(colortext.yellow("LuaRocks is not installed, installing..."))
        install_luarocks()
    if check_moonscript() == False:
        print(colortext.yellow("MoonScript is not installed, installing..."))
        install_moonscript()
        
# CONFIG
def getconfig(lang, key):
  script_dir = os.path.dirname(os.path.realpath(__file__))
  try:
    with open(os.path.join(script_dir, "cfg.pkl"), "rb") as file:
      return pickle.load(file)[lang][key]
  except EOFError:
    # the file is empty, write {} to it
    with open(os.path.join(script_dir, "cfg.pkl"), "wb") as file:
      pickle.dump({}, file)

    return None
def setconfig(lang, key, value):
  script_dir = os.path.dirname(os.path.realpath(__file__))
  try:
    with open(os.path.join(script_dir, "cfg.pkl"), "rb") as file:
      cfg = pickle.load(file)
      if not lang in cfg:
        cfg[lang] = {}
      cfg[lang][key] = value
      with open(os.path.join(script_dir, "cfg.pkl"), "wb") as file:
        pickle.dump(cfg, file)
  except EOFError:
    # the file is empty, write {} to it
    with open(os.path.join(script_dir, "cfg.pkl"), "wb") as file:
      pickle.dump({}, file)
      


# UTIL
def backwordreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)


# INTERFACE
def p():
  print("The plugin is decreapted. Please use the CLI alongside a Studio+VSCode sync plugin.")
  @app.route('/', methods=["GET", "POST"]) 
  def base_page():
    code = (request.data).decode()
    try:
      lua_code = translator.translate(code)
    except Exception as e:
      return "CompileError!:"+str(e)

    return lua_code

  @app.route('/err', methods=["GET", "POST"]) 
  def debug():
    code = (request.data).decode()
    rep = Reporter()
    num = str(api.check(code, "roblox.py", rep))
    print(num)
    return rep.diagnostics

  @app.route("/lib", methods=["GET"]) 
  def library():
      return translator.getluainit()
    
  app.run(
  host='0.0.0.0', 
  port=5555 
  )

def w():
  try:
    def incli():
      # NOTE: Since this isnt packaged yet, using this will only check files inside of the test folder

      # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
      path = os.getcwd()

      for r, d, f in os.walk(path):
        for file in f:
            if '.py' in file:
              # compile the file to a file with the same name and path but .lua
              contents = ""
              
              try:
                with open(os.path.join(r, file)) as rf:
                  contents = rf.read()  
              except Exception as e:
                print(colortext.red(f"Failed to read {os.path.join(r, file)}!\n\n "+str(e)))
                # do not compile the file if it cannot be read
                continue
              
              try:
                lua_code = translator.translate(contents)
                print(colortext.green("roblox-py: Compiled "+os.path.join(r, file)))
                # get the relative path of the file and replace .py with .lua
                relative_path = backwordreplace(os.path.join(r, file),".py", ".lua", 1)
                
                if not os.path.exists(os.path.dirname(relative_path)):
                  open(os.path.dirname(relative_path), "x").close()
                with open(relative_path, "w") as f:
                  f.write(lua_code)
              except Exception as e:
                print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)))
              

      action = input("")
      if action == "exit":
        exit(0)
      else:
        incli()
    
    if sys.argv.__len__() >= 1:
      if sys.argv[1] == "p":
        p()
      elif sys.argv[1] == "lib":
        # sys.argv[2] is the path to the file, create a new file there with the name robloxpyc.lua, and write the library to it
        try:
          cwd = os.getcwd()
          # cwd+sys.argv[2]
          dir = os.path.join(cwd, sys.argv[2])
          
          open(dir, "x").close()
          with open(dir, "w") as f:
            f.write(translator.getluainit())
        except IndexError:
          if getconfig("general", "defaultlibpath") != "" and getconfig("general", "defaultlibpath") != None:
            print(colortext.red("roblox-py: No path specified!"))
          else:
             cwd = os.getcwd()
             # cwd+sys.argv[2]
             dir = os.path.join(cwd, getconfig("general", "defaultlibpath"))
              
             open(dir, "x").close()
             with open(dir, "w") as f:
               f.write(translator.getluainit())
      elif sys.argv[1] == "c":
        # Go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(colortext.yellow("Are you sure? This will delete all .lua files and add a .py file with the same name.\n\nType 'yes' to continue."))
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
                print(colortext.green("roblox-py: Converted to py "+os.path.join(r, file)+" as "+file.replace(".lua", ".py")))
      elif sys.argv[1] == "w":
        print(colortext.magenta("roblox-py: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
      elif sys.argv[1] == "t":
        luainit.generatewithlibraries()
      else:
        print(colortext.magenta("roblox-py: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
    else:
      print(colortext.magenta("roblox-py: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
      incli()
  except IndexError:
    print(colortext.red("roblox-py: Invalid amount of arguments!"))
  except KeyboardInterrupt:
    print(colortext.red("roblox-py: Aborted!"))
def cw():
  try:
    print(colortext.yellow("roblox-c: Note, this is not yet completed and will not work and is just a demo to show the AST and very light nodevisitor. A production version will be released soon."))
    def incli():
      # NOTE: Since this isnt packaged yet, using this will only check files inside of the test folder

      # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
      path = os.getcwd()

      for r, d, f in os.walk(path):
        for file in f:
            if '.c' in file and not '.cpp' in file:
              # compile the file to a file with the same name and path but .lua
              try:
                newctranslator = parser.CodeConverter("name.c")
                newctranslator.parse(
                  os.path.join(r, file),
                  # C not C++
                  flags=[
                      '-I%s' % inc for inc in []
                  ] + [
                      '-D%s' % define for define in []
                  ] + [
                      '-std=%s' % getconfig("c", "std")
                  ] + [
                      '-stdlib=%s' % getconfig("c", "stdlib")
                  ] + [
                    '-L=%s' % getconfig("c", "dynamiclibpath")
                  ]
                )
                
                newctranslator.diagnostics(sys.stderr)
                relative_path = backwordreplace(os.path.join(r, file),".c", ".lua", 1)
                with open(relative_path, 'w') as out:
                  newctranslator.output(relative_path, out)
                  
                print(colortext.green("roblox-c: Compiled "+os.path.join(r, file)))
              except Exception as e:
                print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)))
              

      action = input("")
      if action == "exit":
        exit(0)
      else:
        incli()
    
    if sys.argv.__len__() >= 1:
      if sys.argv[1] == "p":
        print(colortext.red("roblox-c: Plugins are only supported for python!"))
      elif sys.argv[1] == "lib":
        # sys.argv[2] is the path to the file, create a new file there with the name robloxpyc.lua, and write the library to it
        try:
          cwd = os.getcwd()
          # cwd+sys.argv[2]
          dir = os.path.join(cwd, sys.argv[2])
          open(dir, "x").close()
          with open(dir, "w") as f:
            f.write(translator.get_luainit())
        except IndexError:
          if getconfig("general", "defaultlibpath") != "" and getconfig("general", "defaultlibpath") != None:
            print(colortext.red("roblox-c: No path specified!"))
          else:
             cwd = os.getcwd()
             # cwd+sys.argv[2]
             dir = os.path.join(cwd, getconfig("general", "defaultlibpath"))
              
             open(dir, "x").close()
             with open(dir, "w") as f:
               f.write(translator.get_luainit())
      elif sys.argv[1] == "c":
        # Go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(colortext.yellow("Are you sure? This will delete all .lua files and add a .c file with the same name.\n\nType 'yes' to continue."))
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
                print(colortext.green("roblox-c: Converted to c "+os.path.join(r, file)+" as "+file.replace(".lua", ".c")))
      elif sys.argv[1] == "w":
        print(colortext.magenta("roblox-c: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
      else:
        print(colortext.magenta("roblox-c: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
    else:
      print(colortext.magenta("roblox-c: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
      incli()
  except IndexError:
    print(colortext.red("roblox-c: Invalid amount of arguments!"))
  except KeyboardInterrupt:
    print(colortext.red("roblox-c: Aborted!"))
     
def cpw():
  try:
    print(colortext.yellow("roblox-cpp: Note, this is not yet completed and will not work and is just a demo to show the AST and very light nodevisitor. A production version will be released soon."))
    def incli():
      # NOTE: Since this isnt packaged yet, using this will only check files inside of the test folder

      # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
      path = os.getcwd()

      for r, d, f in os.walk(path):
        for file in f:
            if '.cpp' in file:
              # compile the file to a file with the same name and path but .lua
              try:
                newctranslator = parser.CodeConverter("name.cpp")
                newctranslator.parse(
                  os.path.join(r, file),
                  flags=[
                      '-I%s' % inc for inc in []
                  ] + [
                      '-D%s' % define for define in []
                  ] + [
                      '-std=%s' % getconfig("cpp", "std")
                  ] + [
                      '-stdlib=%s' % getconfig("cpp", "stdlib")
                  ]
                )
                
                newctranslator.diagnostics(sys.stderr)
                relative_path = backwordreplace(os.path.join(r, file),".cpp", ".lua", 1)
                with open(relative_path, 'w') as out:
                  newctranslator.output(relative_path, out)
                  
                print(colortext.green("roblox-cpp: Compiled "+os.path.join(r, file)))
              except Exception as e:
                print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)))
              

      action = input("")
      if action == "exit":
        exit(0)
      else:
        incli()
    
    if sys.argv.__len__() >= 1:
      if sys.argv[1] == "p":
        print(colortext.red("roblox-cpp: Plugins are only supported for python!"))
      elif sys.argv[1] == "lib":
        # sys.argv[2] is the path to the file, create a new file there with the name robloxpyc.lua, and write the library to it
        try:
          cwd = os.getcwd()
          # cwd+sys.argv[2]
          dir = os.path.join(cwd, sys.argv[2])
          open(dir, "x").close()
          with open(dir, "w") as f:
            f.write(translator.get_luainit())
        except IndexError:
          if getconfig("general", "defaultlibpath") != "" and getconfig("general", "defaultlibpath") != None:
            print(colortext.red("roblox-cpp: No path specified!"))
          else:
             cwd = os.getcwd()
             # cwd+sys.argv[2]
             dir = os.path.join(cwd, getconfig("general", "defaultlibpath"))
              
             open(dir, "x").close()
             with open(dir, "w") as f:
               f.write(translator.get_luainit())
      elif sys.argv[1] == "c":
        # Go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(colortext.yellow("Are you sure? This will delete all .lua files and add a .cpp file with the same name.\n\nType 'yes' to continue."))
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
                
                print(colortext.green("roblox-cpp: Converted to c++ "+os.path.join(r, file)+" as "+file.replace(".lua", ".cpp")))
      elif sys.argv[1] == "w":
        print(colortext.magenta("roblox-cpp: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
      else:
        print(colortext.magenta("roblox-cpp: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
    else:
      print(colortext.magenta("roblox-cpp: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
      incli()
  except IndexError:
    print(colortext.red("roblox-cpp: Invalid amount of arguments!"))
  except KeyboardInterrupt:
    print(colortext.red("roblox-cpp: Aborted!"))
    
def lunar():
  try:
    checkboth() # install luarocks and moonscript if not installed
    def incli():
      # NOTE: Since this isnt packaged yet, using this will only check files inside of the test folder

      # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
      path = os.getcwd()

      for r, d, f in os.walk(path):
        for file in f:
            if '.moon' in file:
              # compile the file to a file with the same name and path but .lua
                # Run command and check if anything is outputted to stderr, stdout, or stdin
                
                stdout, stderr = subprocess.Popen(["moonc", os.path.join(r, file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                if stdout or stderr:
                  if stdout:
                    print(colortext.red("Compile Error for "+os.path.join(r, file)+"!\n\n "+str(stdout)))
                  else:
                    print(colortext.red("Compile Error for "+os.path.join(r, file)+"!\n\n "+str(stderr)))
                else:
                  try:
                    newheader = header.lunarheader(luainit.lunarfunctions)
                    
                    # check if the new file has been created
                    if os.path.exists(os.path.join(r, file.replace(".moon", ".lua"))):
                      print(colortext.green("roblox-lunar: Compiled "+os.path.join(r, file)))
                      
                      with open(os.path.join(r, file.replace(".moon", ".lua")), "r") as f:
                        contents = f.read()
                      with open(os.path.join(r, file.replace(".moon", ".lua")), "w") as f:
                        f.write(newheader+contents)
                    else:
                      print(colortext.red("File error for "+os.path.join(r, file)+"!"))
                  except Exception as e:
                    print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)))
              

      action = input("")
      if action == "exit":
        exit(0)
      else:
        incli()
    
    if sys.argv.__len__() >= 1:
      if sys.argv[1] == "p":
        print(colortext.red("roblox-lunar: Plugins are only supported for python!"))
      elif sys.argv[1] == "lib":
        # sys.argv[2] is the path to the file, create a new file there with the name robloxpyc.lua, and write the library to it
        try:
          cwd = os.getcwd()
          # cwd+sys.argv[2]
          dir = os.path.join(cwd, sys.argv[2])
          open(dir, "x").close()
          with open(dir, "w") as f:
            f.write(translator.get_luainit())
        except IndexError:
          if getconfig("general", "defaultlibpath") != "" and getconfig("general", "defaultlibpath") != None:
            print(colortext.red("roblox-lunar: No path specified!"))
          else:
             cwd = os.getcwd()
             # cwd+sys.argv[2]
             dir = os.path.join(cwd, getconfig("general", "defaultlibpath"))
              
             open(dir, "x").close()
             with open(dir, "w") as f:
               f.write(translator.get_luainit())
      elif sys.argv[1] == "c":
        # Go through every lua descendant file in the current directory and delete it and create a new file with the same name but .py
        confirm = input(colortext.yellow("Are you sure? This will delete all .lua files and add a .moon file with the same name.\n\nType 'yes' to continue."))
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
                
                print(colortext.green("roblox-lunar: Converted to lunar "+os.path.join(r, file)+" as "+file.replace(".lua", ".moon")))
      elif sys.argv[1] == "w":
        print(colortext.magenta("roblox-lunar: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
      else:
        print(colortext.magenta("roblox-lunar: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
        incli()
    else:
      print(colortext.magenta("roblox-lunar: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
      incli()
  except IndexError:
    print(colortext.red("roblox-lunar: Invalid amount of arguments!"))
  except KeyboardInterrupt:
    print(colortext.red("roblox-lunar: Aborted!"))
        

def pyc():
  title = colortext.magenta("roblox-pyc")
  py = colortext.blue("roblox-py")
  c = colortext.blue("roblox-c")
  cpp = colortext.blue("roblox-cpp")
  lunar = colortext.blue("roblox-lunar")
  border = colortext.white("--------------------")
  blank = colortext.blue("roblox-")+colortext.magenta("<lang>")
  blankpath = colortext.magenta("<path>")
  selftool = colortext.blue("roblox-pyc")
  
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
3 - Change dynamic library path
              """)
        
        inputval = input("Select which config to open: ")
        if inputval == "1":
          returned = input("Enter the std: ")
          setconfig("c", "std", returned)
        elif inputval == "2":
          returned = input("Enter the stdlib: ")
          setconfig("c", "stdlib", returned)
        elif inputval == "3":
          returned = input("Enter the dynamic library path: ")
          setconfig("c", "dynamiclibpath", returned)
      elif returnval == "3":
        print(f"""
Configuring {cpp}
{border}
1 - Change std 
2 - Change stdlib
3 - Change dynamic library path
              """)
        
        inputval = input("Select which config to open: ")
        if inputval == "1":
          returned = input("Enter the std: ")
          setconfig("cpp", "std", returned)
        elif inputval == "2":
          returned = input("Enter the stdlib: ")
          setconfig("cpp", "stdlib", returned)
        elif inputval == "3":
          returned = input("Enter the dynamic library path: ")
          setconfig("cpp", "dynamiclibpath", returned)
      elif returnval == "4":
        print(f"{lunar} doesnt need to be configured!")
      elif returnval == "5":
        print("""
Configuring General
{border}
1 - Change default lib path
              """)
        inputval = input("Select which config to open: ")
        if inputval == "1":
          returned = input("Enter the default lib path: ")
          setconfig("general", "defaultlibpath", returned)
      else:
        print(colortext.red("Invalid option!"))
    elif sys.argv[1] == "devforum":
      webbrowser.open("https://devforum.com")
    elif sys.argv[1] == "discord":
      webbrowser.open("https://discord.gg/jbMFyBcBC2")
    elif sys.argv[1] == "github":
      webbrowser.open("https://github.com/AsynchronousAI/roblox-pyc")
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
  {border}
  CLI DOCS:
  - {blank} w - Click enter in the terminal to compile all scripts
  - {blank} p - Start the plugin server (only for {py})
  - {blank} lib {blankpath} - Get the library file for language and write it to the path (path has to include filename)
  - {blank} c - Convert all .lua files to targeted language files, it will comment the existing lua code
  - {selftool} config - Open the config menu
  - {selftool} devforum - Open the devforum page in a browser
  - {selftool} discord - Open the discord server in a browser
  - {selftool} github - Open the github page in a browser
  {border}
  MORE HELP:
  - Devforum
  - Discord
  - Github Issues

          """)
  except KeyboardInterrupt:
    print(colortext.red("roblox-pyc: Aborted!"))  
if __name__ == "__main__":
  print(colortext.blue("Test mode"))
  mode = input("Select which app to run (1, 2, 3): ")
  
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