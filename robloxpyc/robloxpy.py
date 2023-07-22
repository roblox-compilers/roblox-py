# PYPI 
from flask import Flask, request
from pyflakes import api
from packaging import version
from tqdm import tqdm
from time import sleep

# FILES
from . import pytranslator, colortext, luainit, parser, ctranslator, header #ctranslator is old and not used

# BUILTIN
import subprocess,shutil,sys,threading,json,requests,traceback,pkg_resources,re,sys,webbrowser,pickle, os, zipfile

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
global count
count = 0

try:
  registry = json.loads(requests.get(registryrawurl).text)
except json.JSONDecodeError:
  print(colortext.white("Import will not work, registry is corrupted. Please report this issue to the github repo, discord server, or the devforum post\nthanks!"))
  registry = {} 

# LOADING
class loader:
  self = {}
  def __init__(self, max):
    print("\n\n")
    self.max = max
    self.current = 0
    self.tqdm = tqdm(total=max)
    
  def yielduntil(self):
    global count
    while self.max != self.current:
      sleep(.5)
    self.tqdm.update(self.max-self.current )
    self.tqdm.close()
  def update(self, amount):
    self.tqdm.update(amount)

# ERROR
def candcpperror():
  print(warn("C and C++ are not supported in this build, coming soon! \n\n contributions on github will be greatly appreciated!"))
def error(errormessage, source=""):
  if source != "":
    source = colortext.white(" ("+source+") ")
  if getconfig("general", "goofy", False):
    subprocess.call(["say", errormessage])
  return(colortext.red("error ", ["bold"])+source+errormessage)
def warn(warnmessage, source=""):
  if source != "":
    source = colortext.white(" ("+source+") ")
  return(colortext.yellow("warning ", ["bold"])+source+warnmessage)
def info(infomessage, source=""):
  if source != "":
    source = colortext.white(" ("+source+") ")
  return(colortext.blue("info ", ["bold"])+source+infomessage)
def debug(infomessage):
  if getconfig("general", "traceback", False):
    print(colortext.blue("debug ", ["bold"])+infomessage)
    print(traceback.format_exc())
def decreapted(source=""):
  if source != "":
    source = colortext.white(" ("+source+") ")
  print(colortext.yellow("decreapted ", ["bold"])+source+"This feature is decreapted and will be removed in a future version of roblox-pyc")
# INSTALL ROBLOX-TS
def check_npms():
  try:
    subprocess.call(["npm", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    return True
  except FileNotFoundError:
    return False
def check_roblox_ts():
  try:
    subprocess.call(["rbxtsc", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
    return True
  except FileNotFoundError:
    return False
def install_npms():
  print("Installing npm...")
  if sys.platform == "linux":
    subprocess.call(["apt-get", "install", "-y", "npm"])
  elif sys.platform == "darwin":
    subprocess.call(["brew", "install", "npm"])
  elif sys.platform == "win32":
    subprocess.call(["choco", "install", "npm"])
  else:
    print(error("Could not auto-install npm, please install it manually."))
def install_roblox_ts():
  print("Installing roblox-ts...")
  subprocess.call(["npm", "install", "-g", "roblox-ts"])

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
    print(error("Could not auto-install llvm, please install it manually."))
def config_llvm(home=None, lib=None):
  if home and home != "None":
    subprocess.call(["export", "LLVM_HOME="+home])
  if lib and lib != "None":
    subprocess.call(["export", "LD_LIBRARY_PATH="+lib])

  # check if wally is installed, if they are in mac use brew otherwise error
  try:
    subprocess.call(["wally", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
  except FileNotFoundError:
    if sys.platform == "darwin":
      print(info("Installing wally..."))
      subprocess.call(["brew", "install", "wally"])
    else:
      print(error("Wally was not found and could not be auto-installed. Please install it manually."))
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
        print(warn("LuaRocks is not installed, installing..."))
        install_luarocks()
    if check_moonscript() == False:
        print(warn("MoonScript is not installed, installing..."))
        install_moonscript()
        
# CONFIG
def getconfig(lang, key, default=None):
  script_dir = os.path.dirname(os.path.realpath(__file__))
  try:
    with open(os.path.join(script_dir, "cfg.pkl"), "rb") as file:
      try:
        returnval = pickle.load(file)[lang][key]
        if returnval == None or returnval == "":
          #print("Returned default because value was None or empty")
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
          print(error("Config file KeyError!", "roblox-py"))
          return default
    
        # Write the missing lang or key in and return the default
        if bugged == "lang":
          #print(warn("Adding missing language %s to config file..." % lang))
          new = pickle.load(file)
          new[lang] = {}
          pickle.dump(new, file)
        if bugged == "key":
          #print(warn("Adding missing key %s to config file..." % key))
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
    print(info(f"Update available to {latest_version}, you are currently using {current_version}"))
    choice = input("\t\tDo you want to update? (yes/no): ").lower()
    if choice == "yes":
      # Add the pip upgrade command here.
      subprocess.run(["pip", "install", f"roblox-pyc=={latest_version}"])

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
  open(os.path.join(os.getcwd(), "dependencies", author+"_"+name+".zip"), "x").close()
  with open(os.path.join(os.getcwd(), "dependencies", author+"_"+name+".zip"), "wb") as file:
    file.write(response)
  # unzip
  print(info("Unzipping package...", "roblox-pyc wally"))
  with zipfile.ZipFile(os.path.join(os.getcwd(), "dependencies", author+"_"+name+".zip"), 'r') as zip_ref:
    zip_ref.extractall(os.path.join(os.getcwd(), "dependencies", author+"_"+name))
  # delete the zip
  print(info("Deleting uneeded resources...", "roblox-pyc wally"))
  os.remove(os.path.join(os.getcwd(), "dependencies", author+"_"+name+".zip"))

# JSON 
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

# CLI PACKAGES
def onNotFound(target):
  currentcommand = sys.argv[2]
  
  allCLIS = getconfig("general", "cli", [])
  
  # go through allCLIS and check if target and command matches
  for i in allCLIS:
    if i["target"] == target:
      pass
def lib():
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
        f.write(translator.get_luainit(getconfig("general", "luaext", [])))
  
# ASYNC 
def filtercompiledfolder():
  cwd = os.getcwd()
  compiled = cwd+"-compiled"
  for r, d, f in os.walk(compiled):
    for file in f:
      if not file.endswith(".lua"):
        os.remove(os.path.join(r, file))
     
def unknowncompile(r, file):
  if file.endswith(".txt") or ("." not in file):
     # This is for text files and files without a file extension
    try:
      contents = ""
      with open(os.path.join(r, file), "r") as f:
        contents = f.read()
        contents = contents.replace("]]", "]\]")
        contents = "--/ Compiled using roblox-pyc | Textfile compiler \--\nreturn {Contents = [["+contents+"]], Type = 'rawtext', Extension = '"+file.split(".")[file.split(".").__len__()-1]+"'}"
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
  if file.endswith(".json") and not(file == "package.json" or file == "tsconfig.json" or file == "default.project.json"):
    # compile the file to a file with the same name and path but .lua
    try:
      contents = ""
      with open(os.path.join(r, file), "r") as f:
        contents = f.read()
        contents = "--/ Compiled using roblox-pyc | JSON compiler \--\nreturn {Contents = "+json_to_lua(contents)+", Type = 'json', Extension = 'json'}"
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
        # Just delete the file
        print(warn("Failed to read "+os.path.join(r, file)+"!"))
def othercompile(r, file): # Handles Text files and JSON files, and files without a file extension
  jsoncompile(r, file)
  unknowncompile(r, file)
def cppcompile(r, file, pluscount=False):
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
      path = os.path.join(r, file)  
      newctranslator.diagnostics(sys.stderr)
      relative_path = backwordreplace(path,".cpp", ".lua", 1)
      with open(relative_path, 'w') as out:
        newctranslator.output(relative_path, out)   
                  
        #print(colortext.green("Compiled "+os.path.join(r, file)))
      if pluscount:
        pluscount.update(1)
        pluscount.current += 1
        #global count
        #count += 1
    except Exception as e:
      if "To provide a path to libclang use Config.set_library_path() or Config.set_library_file()" in str(e):
        print(error("dylib not found, use `roblox-pyc config`, c++, dynamiclibpath, and set the path to the dynamic library."))
      print(error(f"Compile Error!\n\n "+str(e), f"{os.path.join(r, file)}"))
      debug("Compiler error "+str(e))
      returnval = input("Do you want to continue? (yes/no): ").lower()
      if returnval == "no":
        sys.exit()
      else:
        if pluscount:
          pluscount.update(1)
          pluscount.current += 1
          #global count
          #count += 1
        return
        
def ccompile(r, file, pluscount=False):
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
      path = os.path.join(r, file)  
                
      newctranslator.diagnostics(sys.stderr)
      relative_path = backwordreplace(path,".c", ".lua", 1)
      
      with open(relative_path, 'w') as out:
        newctranslator.output(relative_path, out)
                  
        #print(colortext.green("Compiled "+os.path.join(r, file)))
      if pluscount:
        pluscount.update(1)
        pluscount.current += 1
        #global count
        #count += 1
    except Exception as e:
      if "To provide a path to libclang use Config.set_library_path() or Config.set_library_file()" in str(e):
        print(error("dylib not found, use `roblox-pyc config`, c, dynamiclibpath, and set the path to the dynamic library."))
      print(error(f"Compile Error!\n\n "+str(e), f"{os.path.join(r, file)}"))
      debug("Compile error at "+str(e))
      returnval = input("Do you want to continue? (yes/no): ").lower()
      if returnval == "no":
        sys.exit()
      else:
        if pluscount:
          pluscount.update(1)
          pluscount.current += 1
          #global count
          #count += 1
        return
def pycompile(r, file, pluscount=False):
  if file.endswith(".py"):
    # compile the file to a file with the same name and path but .lua
    contents = ""
              
    try:
      with open(os.path.join(r, file)) as rf:
        contents = rf.read()  
    except Exception as e:
      print(error(f"Failed to read {os.path.join(r, file)}!\n\n "+str(e)))
      # do not compile the file if it cannot be read
      return
              
    try:
      translator = pytranslator.Translator()
      lua_code = translator.translate(contents)
      #print(colortext.green("Compiled "+os.path.join(r, file)))
      # get the relative path of the file and replace .py with .lua
      path = os.path.join(r, file)  
        
      relative_path = backwordreplace(path,".py", ".lua", 1)
      
      if not os.path.exists(os.path.dirname(relative_path)):
        os.makedirs(os.path.dirname(relative_path))
      
      with open(relative_path, "w") as f:
        f.write(lua_code)
      
      if pluscount:
        pluscount.update(1)
        pluscount.current += 1
        #global count
        #count += 1
    except Exception as e:
      print(error(f"Compile Error!\n\n "+str(e), f"{os.path.join(r, file)}"))
      debug("Compile error at "+str(e))
      returnval = input("Do you want to continue? (yes/no): ").lower()
      if returnval == "no":
        sys.exit()
      else:
        if pluscount:
          pluscount.update(1)
          pluscount.current += 1
          #global count
          #count += 1
        return
def lunarcompile(r, file, pluscount=False):
  if file.endswith(".moon"):
    # compile the file to a file with the same name and path but .lua
    # Run command and check if anything is outputted to stderr, stdout, or stdin
                
    process = subprocess.Popen(["moonc", os.path.join(r, file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
                
    if stdout or stderr:
      if stdout:     
        print(error(f"Compile Error!\n\n "+str(stdout), f"{os.path.join(r, file)}"))
        returnval = input("Do you want to continue? (yes/no): ").lower()
        if returnval == "no":
          sys.exit()
        else:
          if pluscount:
            pluscount.update(1)
            pluscount.current += 1
            #global count
            #count += 1
          return
      else:
        print(error(f"Compile Error!\n\n "+str(stderr), f"{os.path.join(r, file)}"))
        returnval = input("Do you want to continue? (yes/no): ").lower()
        if returnval == "no":
          sys.exit()
        else:
          if pluscount:
            pluscount.update(1)
            pluscount.current += 1
            #global count
            #count += 1
          return
    else:
      try:
        newheader = header.lunarheader(luainit.lunarfunctions)
                    
        # check if the new file has been created
        if os.path.exists(os.path.join(r, file.replace(".moon", ".lua"))):
          #print(colortext.green("Compiled "+os.path.join(r, file)))          
          with open(os.path.join(r, file.replace(".moon", ".lua")), "r") as f:
            contents = f.read()
          with open(os.path.join(r, file.replace(".moon", ".lua")), "w") as f:
            f.write(newheader+contents)
          
        else:
          print(error("File error for "+os.path.join(r, file)+"!"))
        if pluscount:
          pluscount.update(1)
          pluscount.current += 1
          #global count
          #count += 1
      except Exception as e:
          print(error(f"Compile Error!\n\n "+str(e), f"{os.path.join(r, file)}"))
          returnval = input("Do you want to continue? (yes/no): ").lower()
          if returnval == "no":
            sys.exit()
          else:
            if pluscount:
              pluscount.update(1)
              pluscount.current += 1
              #global count
              #count += 1
            return
def robloxtscompile(r, file, pluscount=False):
  if file.endswith(".ts") or file.endswith(".tsx"):
    # Just add to pluscount, add later
    try:
      print(warn("At the moment roblox-ts is not supported, please wait for a future update."))
      if pluscount:
        pluscount.update(1)
        pluscount.current += 1
        #global count
        #count += 1
    except Exception as e:
        print(error(f"Compile Error!\n\n "+str(e), f"{os.path.join(r, file)}"))
        returnval = input("Do you want to continue? (yes/no): ").lower()
        if returnval == "no":
          sys.exit()
        else:
          if pluscount:
            pluscount.update(1)
            pluscount.current += 1
            #global count
            #count += 1
          return
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

# TODO: Add thread count system to 
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
      print(colortext.green("Compiled "+str(count)+" files!"))
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
      print(colortext.green("Compiled "+str(count)+" files!"))
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
          path = os.getcwd()
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
# NOTE: Since C and C++ are disabled, their features are out of sync with python and lunar
def cw():
  if not check_llvm():
    install_llvm()
  
  config_llvm(getconfig("c", "llvmhome", "None"), getconfig("c", "libclangpath", "None"))
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
      print(colortext.green("Compiled "+str(count)+" files!"))
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
      print(colortext.green("Compiled "+str(count)+" files!"))
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
          path = os.getcwd()
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
  if not check_llvm():
    install_llvm()
  
  config_llvm(getconfig("c", "llvmhome", "None"), getconfig("c", "libclangpath", "None"))
  
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
      print(colortext.green("Compiled "+str(count)+" files!"))
      
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
      print(colortext.green("Compiled "+str(count)+" files!"))
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
          path = os.getcwd()
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
      print(colortext.green("Compiled "+str(count)+" files!"))
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
      print(colortext.green("Compiled "+str(count)+" files!"))
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
          path = os.getcwd()
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
  print(colortext.green("Compiled "+str(count)+" files!"))
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
  print(colortext.green("Compiled "+str(count)+" files!"))
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
      webbrowser.open("https://discord.gg/jbMFyBcBC2")
    elif sys.argv[1] == "github":
      webbrowser.open("https://github.com/AsynchronousAI/roblox-pyc")
    elif sys.argv[1] == "help":
      raise IndexError
    elif sys.argv[1] == "w":
      print(colortext.magenta("Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)))+" ...\n Type 'exit' to exit, Press enter to compile."))
      globalincli()
    elif sys.argv[1] == "d":
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
      print(error("Cannot replace all files for a general language, please specify a language by using rbxpy, rbxlun, rbxc, rbxcpp", "roblox-pyc"))
    elif sys.argv[1] == "tsc":
      # Pretty much c but for typescript and works
      if not check_roblox_ts():
        if not check_npms():
          install_npms()
        install_roblox_ts()
      confirm = input(warn("Are you sure? This will delete all .lua files and add a .ts file with the same name.\n\nType 'yes' to continue."))
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