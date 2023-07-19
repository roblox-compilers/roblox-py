import os
from flask import Flask, request
from pyflakes import api
import re
import sys
import webbrowser
import pickle
from . import pytranslator, colortext, luainit, parser, ctranslator, header #ctranslator is old and not used
import subprocess
import shutil
import sys
import threading
import json
import requests 
from packaging import version
import pkg_resources

class Reporter:
    """
    Formats the results of pyflakes checks to users.
    """
    def __init__(self):
        self.diagnostics = []

    def unexpectedError(self, filename, msg):
        """
        An unexpected error occurred attemptinh to process C{filename}.

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
registryrawurl = "https://raw.githubusercontent.com/roblox-pyc/registry/main/registry.json"

try:
  registry = json.loads(requests.get(registryrawurl).text)
except json.JSONDecodeError:
  print(colortext.red("roblox-py: Import will not work, registry is corrupted. Please report this issue to the github repo, discord server, or the devforum post\nthanks!"))
  registry = {} 
  
# INSTALL SEALANG
def check_llvm():
  return True # Add LLVM check/installs later
def install_llvm():
  print("Installing LLVM...")
  if sys.platform == "linux":
    subprocess.call(["apt-get", "install", "-y", "llvm"])
  elif sys.platform == "darwin":
    subprocess.call(["brew", "install", "llvm", "--with-clang", "--with-asan"])
  elif sys.platform == "win32":
    subprocess.call(["choco", "install", "llvm"])
  else:
    print(colortext.red("Could not auto-install llvm, please install it manually."))
def config_llvm(home=None, lib=None):
  if home and home != "None":
    subprocess.call(["export", "LLVM_HOME="+home])
  if lib and lib != "None":
    subprocess.call(["export", "LD_LIBRARY_PATH="+lib])
    
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
def getconfig(lang, key, default=None):
  script_dir = os.path.dirname(os.path.realpath(__file__))
  try:
    with open(os.path.join(script_dir, "cfg.pkl"), "rb") as file:
      try:
        returnval = pickle.load(file)[lang][key]
        if returnval == None or returnval == "":
          print("Returned default because value was None or empty")
          return default
        else:
          return returnval
      except KeyError:
        # find which one doesnt exist, lang or key
        bugged = ""
        try:
          test = pickle.load(file)[lang]
        except KeyError:
          bugged = "lang"
        if bugged == "":
          try:
            test = pickle.load(file)[lang][key]
          except KeyError:
            bugged = "key"
        if bugged == "": 
          print(colortext.red("roblox-py: Config file KeyError!"))
          return default
    
        # Write the missing lang or key in and return the default
        if bugged == "lang":
          #print(colortext.yellow("roblox-py: Adding missing language %s to config file..." % lang))
          new = pickle.load(file)
          new[lang] = {}
          pickle.dump(new, file)
        if bugged == "key":
          #print(colortext.yellow("roblox-py: Adding missing key %s to config file..." % key))
          new = pickle.load(file)
          new[lang][key] = default
          pickle.dump(new, file)
        
        print("Returned default because key or lang was missing and I added it")
        return default
  except EOFError:
    # the file is empty, write {} to it
    with open(os.path.join(script_dir, "cfg.pkl"), "wb") as file:
      pickle.dump({}, file)

    return default
def setconfig(lang, key, value, default=None):
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
  except KeyError:
    # this is now getconfigs problem i dont give a shit no more
    getconfig(lang, key, default)

# UPDATES
def get_latest_version():
    url = f"https://pypi.org/pypi/roblox-pyc/json"
    response = requests.get(url)
    data = response.json()
    return data["info"]["version"]

def check_for_updates():
  current_version = pkg_resources.get_distribution("roblox-pyc").version
  latest_version = get_latest_version()
  if version.parse(latest_version) > version.parse(current_version):
    print(f"Update available to {latest_version}, you are currently using {current_version}")
    choice = input("Do you want to update? (yes/no): ").lower()
    if choice == "yes":
      # Add the pip upgrade command here.
      subprocess.run(["pip", "install", f"roblox-pyc=={latest_version}"])
      
# CLI PACKAGES
def onNotFound(target):
  currentcommand = sys.argv[2]
  
  allCLIS = getconfig("general", "cli", [])
  
  # go through allCLIS and check if target and command matches
  for i in allCLIS:
    if i["target"] == target:
      pass

# ASYNC 
def cppcompile(r, file):
  if '.cpp' in file and file.endswith(".cpp"):
    # compile the file to a file with the same name and path but .lua
    try:
      newctranslator = parser.CodeConverter(file, getconfig("c", "dynamiclibpath", "None"))
      newctranslator.parse(
      os.path.join(r, file),
      # C not C++
      flags=[
        '-I%s' % inc for inc in []
      ] + [
        '-D%s' % define for define in []
      ] + [
        '-std=%s' % getconfig("cpp", "std", "c++20")
      ] + [
        '-stdlib=%s' % getconfig("cpp", "stdlib", "libc++")
      ]
      )
                
      newctranslator.diagnostics(sys.stderr)
      relative_path = backwordreplace(os.path.join(r, file),".cpp", ".lua", 1)
      with open(relative_path, 'w') as out:
        newctranslator.output(relative_path, out)
                  
        print(colortext.green("roblox-cpp: Compiled "+os.path.join(r, file)))
    except Exception as e:
      if "To provide a path to libclang use Config.set_library_path() or Config.set_library_file()" in str(e):
        print(colortext.red("dylib not found, use `roblox-pyc config`, c++, dynamiclibpath, and set the path to the dynamic library."))
      print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)+" \n\nDEBUG: roblox-pyc error from line "+str(e.__traceback__.tb_lineno)))
def ccompile(r, file):
  if '.c' in file and file.endswith(".c"):
    # compile the file to a file with the same name and path but .lua
    try:
      newctranslator = parser.CodeConverter(file, getconfig("c", "dynamiclibpath", "None"))
      newctranslator.parse(
      os.path.join(r, file),
      # C not C++
      flags=[
        '-I%s' % inc for inc in []
      ] + [
        '-D%s' % define for define in []
      ] + [
        '-std=%s' % getconfig("c", "std", "c11")
      ] + [
        '-stdlib=%s' % getconfig("c", "stdlib", "libc")
      ]
      )
                
      newctranslator.diagnostics(sys.stderr)
      relative_path = backwordreplace(os.path.join(r, file),".c", ".lua", 1)
      with open(relative_path, 'w') as out:
        newctranslator.output(relative_path, out)
                  
        print(colortext.green("roblox-c: Compiled "+os.path.join(r, file)))
    except Exception as e:
      if "To provide a path to libclang use Config.set_library_path() or Config.set_library_file()" in str(e):
        print(colortext.red("dylib not found, use `roblox-pyc config`, c, dynamiclibpath, and set the path to the dynamic library."))
      print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)+" \n\nDEBUG: roblox-pyc error from line "+str(e.__traceback__.tb_lineno)))
def pycompile(r, file):
  if file.endswith(".py"):
    # compile the file to a file with the same name and path but .lua
    contents = ""
              
    try:
      with open(os.path.join(r, file)) as rf:
        contents = rf.read()  
    except Exception as e:
      print(colortext.red(f"Failed to read {os.path.join(r, file)}!\n\n "+str(e)))
      # do not compile the file if it cannot be read
      return
              
    try:
      translator = pytranslator.Translator()
      lua_code = translator.translate(contents)
      print(colortext.green("roblox-py: Compiled "+os.path.join(r, file)))
      # get the relative path of the file and replace .py with .lua
      relative_path = backwordreplace(os.path.join(r, file),".py", ".lua", 1)
                
      if not os.path.exists(os.path.dirname(relative_path)):
        open(os.path.dirname(relative_path), "x").close()
      with open(relative_path, "w") as f:
        f.write(lua_code)
    except Exception as e:
      print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)+" \n\nDEBUG: roblox-pyc error from line "+str(e.__traceback__.tb_lineno)))
def lunarcompile(r, file):
  if file.endswith(".moon"):
    # compile the file to a file with the same name and path but .lua
    # Run command and check if anything is outputted to stderr, stdout, or stdin
                
    process = subprocess.Popen(["moonc", os.path.join(r, file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
                
    if stdout or stderr:
      if stdout:     
        print(colortext.red("Compile Error for "+os.path.join(r, file)+"!\n\n "+stdout.decode("utf-8")))
      else:
        print(colortext.red("Compile Error for "+os.path.join(r, file)+"!\n\n "+stderr.decode("utf-8")))
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
          print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)+" \n\nDEBUG: roblox-pyc error from line "+str(e.__traceback__.tb_lineno)))

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
      translator = pytranslator.Translator()
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
      translator = pytranslator.Translator()
      return translator.get_luainit([])
    
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
          if file.endswith(".py"):
            threading.Thread(target=pycompile, args=(r, file)).start()
            #pycompile(r, file)
              

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
          
          if not os.path.exists(os.path.dirname(dir)):
              open(dir, "x").close()
          with open(dir, "w") as f:
            translator = pytranslator.Translator()
            f.write(translator.get_luainit(getconfig("general", "luaext", [])))
        except IndexError:
          if getconfig("general", "defaultlibpath") != "" and getconfig("general", "defaultlibpath") != None:
            print(colortext.red("roblox-py: No path specified!"))
          else:
             cwd = os.getcwd()
             # cwd+sys.argv[2]
             dir = os.path.join(cwd, getconfig("general", "defaultlibpath"))
             if not os.path.exists(os.path.dirname(dir)):
              open(dir, "x").close()
             with open(dir, "w") as f:
               translator = pytranslator.Translator()
               f.write(translator.get_luainit(getconfig("general", "luaext", [])))
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
  if not check_llvm():
    install_llvm()
  
  config_llvm(getconfig("c", "llvmhome", "None"), getconfig("c", "libclangpath", "None"))
  try:
    print(colortext.yellow("roblox-c: Note, this is not yet completed and will not work and is just a demo to show the AST and very light nodevisitor. A production version will be released soon."))
    def incli():
      # NOTE: Since this isnt packaged yet, using this will only check files inside of the test folder

      # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
      path = os.getcwd()

      for r, d, f in os.walk(path):
        for file in f:
            # check if it ENDS with .c, not if it CONTAINS .c
            # Run use threading 
          if file.endswith(".c"):
            threading.Thread(target=ccompile, args=(r, file)).start()
            #ccompile(r, file)

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
          if not os.path.exists(os.path.dirname(dir)):
              open(dir, "x").close()
          with open(dir, "w") as f:
            translator = pytranslator.Translator()
            f.write(translator.get_luainit(getconfig("general", "luaext", [])))
        except IndexError:
          if getconfig("general", "defaultlibpath") != "" and getconfig("general", "defaultlibpath") != None:
            print(colortext.red("roblox-c: No path specified!"))
          else:
             cwd = os.getcwd()
             # cwd+sys.argv[2]
             dir = os.path.join(cwd, getconfig("general", "defaultlibpath"))
              
             if not os.path.exists(os.path.dirname(dir)):
              open(dir, "x").close()
             with open(dir, "w") as f:
               translator = pytranslator.Translator()
               f.write(translator.get_luainit(getconfig("general", "luaext", [])))
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
  if not check_llvm():
    install_llvm()
  
  config_llvm(getconfig("c", "llvmhome", "None"), getconfig("c", "libclangpath", "None"))
  
  try:
    print(colortext.yellow("roblox-cpp: Note, this is not yet completed and will not work and is just a demo to show the AST and very light nodevisitor. A production version will be released soon."))
    def incli():
      # NOTE: Since this isnt packaged yet, using this will only check files inside of the test folder

      # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
      path = os.getcwd()

      for r, d, f in os.walk(path):
        for file in f:
            if file.endswith(".cpp"):
              # compile the file to a file with the same name and path but .lua
              threading.Thread(target=cppcompile, args=(r, file)).start()
              #cppcompile(r, file)
              

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
          if not os.path.exists(os.path.dirname(dir)):
              open(dir, "x").close()
          with open(dir, "w") as f:
            translator = pytranslator.Translator()
            f.write(translator.get_luainit(getconfig("general", "luaext", [])))
        except IndexError:
          if getconfig("general", "defaultlibpath") != "" and getconfig("general", "defaultlibpath") != None:
            print(colortext.red("roblox-cpp: No path specified!"))
          else:
             cwd = os.getcwd()
             # cwd+sys.argv[2]
             dir = os.path.join(cwd, getconfig("general", "defaultlibpath"))
              
             if not os.path.exists(os.path.dirname(dir)):
              open(dir, "x").close()
             with open(dir, "w") as f:
               translator = pytranslator.Translator()
               f.write(translator.get_luainit(getconfig("general", "luaext", [])))
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
          if file.endswith(".moon"):
            threading.Thread(target=lunarcompile, args=(r, file)).start()
            #lunarcompile(r, file)
              

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
          if not os.path.exists(os.path.dirname(dir)):
              open(dir, "x").close()
          with open(dir, "w") as f:
            translator = pytranslator.Translator()
            f.write(translator.get_luainit(getconfig("general", "luaext", [])))
        except IndexError:
          if getconfig("general", "defaultlibpath") != "" and getconfig("general", "defaultlibpath") != None:
            print(colortext.red("roblox-lunar: No path specified!"))
          else:
             cwd = os.getcwd()
             # cwd+sys.argv[2]
             dir = os.path.join(cwd, getconfig("general", "defaultlibpath"))
              
             if not os.path.exists(os.path.dirname(dir)):
              open(dir, "x").close()
             with open(dir, "w") as f:
               f.write(translator.get_luainit(getconfig("general", "luaext", [])))
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
  blank2 = colortext.blue("rblx-")+colortext.magenta("<lang>")
  blankpath = colortext.magenta("<path>")
  selftool = colortext.blue("roblox-pyc")
  shortselftool = colortext.blue("rblx-pyc")
  shorterselftool = colortext.blue("rpyc")
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
1 - Change default lib path
2 - Change C and C++ dylib
3 - Change LLVM Home Path (only for C and C++)
4 - Change LD-LIBRARY-PATH (only for C and C++)
              """)
        inputval = input("Select which config to open: ")
        if inputval == "1":
          returned = input("Enter the default lib file, it currently is %s: " % getconfig("general", "defaultlibpath"))
          setconfig("general", "defaultlibpath", returned, "")
        elif inputval == "2":
          returned = input("Enter the dynamic library file, it currently is %s: " % getconfig("c", "dynamiclibpath", "None"))
          setconfig("c", "dynamiclibpath", returned, "None")
        elif inputval == "3":
          returned = input("Enter the LLVM Home Path, it currently is %s: " % getconfig("general", "llvmhomepath", "None"))
          setconfig("general", "llvmhomepath", returned, "")
          config_llvm(getconfig("general", "llvmhomepath", ""))
        elif inputval == "4":
          returned = input("Enter the LD-LIBRARY-PATH, it currently is %s: " % getconfig("general", "ldlibrarypath", "None"))
          setconfig("general", "ldlibrarypath", returned, "")
          config_llvm(None, getconfig("general", "ldlibrarypath", ""))
      else:
        print(colortext.red("Invalid option!"))
    elif sys.argv[1] == "devforum":
      webbrowser.open("https://devforum.com")
    elif sys.argv[1] == "discord":
      webbrowser.open("https://discord.gg/jbMFyBcBC2")
    elif sys.argv[1] == "github":
      webbrowser.open("https://github.com/AsynchronousAI/roblox-pyc")
    elif sys.argv[1] == "help":
      raise IndexError
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
            print(colortext.red("roblox-pyc: CLI packages are not supported on this build!"))
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
            os.mkdir(os.path.join(os.getcwd(), "dependencies"))
          
          # Gitclone item["url"] to dependencies folder
          subprocess.call(["git", "clone", item["url"], os.path.join(os.getcwd(), "dependencies", sys.argv[2])])
          print(colortext.green("Installed "+sys.argv[2]+"!"))
      else:
        print(colortext.yellow("roblox-pyc: Package not in registry!")+" install from one of these other package managers:")
        print("""
              1 - luarocks
              2 - pip (compiles to lua)
              3 - pip3 (compiles to lua)
              4 - None
              """)
        returnval = input("Select which package manager to use: ")
        if returnval == "1":
          # install to dependencies folder
          if not check_luarocks():
            install_luarocks()
          subprocess.call(["luarocks", "install", sys.argv[2], "--tree=dependencies"])
        elif returnval == "2":
          # install to dependencies folder
          subprocess.call(["pip", "install", sys.argv[2], "--target=dependencies"])
        elif returnval == "3":
          # install to dependencies folder
          subprocess.call(["pip3", "install", sys.argv[2], "--target=dependencies"])
        else:
          print("Invalid option or exited.")
          return
        
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
            print(colortext.red("roblox-pyc: Module not found!"))
          else:
            setconfig("general", "luaext", currentlist, [])
            print(colortext.green("Uninstalled "+sys.argv[2]+"!"))
        elif type == "package":
          dependenciesPath = os.path.join(os.getcwd(), "dependencies")
          # if it doesnt exist error
          if not os.path.exists(dependenciesPath):
            print(colortext.red("roblox-pyc: Dependencies folder not found! Creating one now..."))
            os.mkdir(dependenciesPath)
            return
          # remove, if not found error
          if not os.path.exists(os.path.join(dependenciesPath, sys.argv[2])):
            print(colortext.red("roblox-pyc: Package not found!"))
          
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
        print(colortext.yellow("roblox-pyc: Dependencies folder not found! Creating one now..."))
        os.mkdir(dependenciesPath)
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
  - {blank} lib {blankpath} - Get the library file for language and write it to the path (path has to include filename)
  - {blank} c - Convert all .lua files to targeted language files, it will comment the existing lua code
  - {blank2} w - Click enter in the terminal to compile all scripts
  - {blank2} p - Start the plugin server (only for {py})
  - {blank2} lib {blankpath} - Get the library file for language and write it to the path (path has to include filename)
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
    print(colortext.red("roblox-pyc: Aborted!"))  
  

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