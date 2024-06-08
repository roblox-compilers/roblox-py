#!/usr/bin/env python3
import sys, ast, os, subprocess, threading, lib, json
from pprint import pprint
from pathlib import Path
from enum import Enum

try:
    import shutil
except ImportError:
    print("Please install the 'shutil' module.")
    exit(1)


#### PYRIGHT ####
def check_pyright(): #TODO: make this into mypy
    exists = shutil.which("pyright") is not None
   # if not exists:
   #     warn("pyright is not installed, install it for more descriptive and compiler errors.")
    return exists

#### COMPILER ####
from luau import *
from binop import *
from boolop import *
from compop import *
from const import *
from context import *
from loopcounter import *
from symbols import *
from tokenend import *
from translator import *
from unary import *
from config import *

#class PyGenerator:
    
#### INTERFACE ####
from log import *

def usage():
    print("\n"+f"""usage: \033[1;33mrbxpy\033[0m [file] [options] -o [gen]
\033[1mOptions:\033[0m
{TAB}\033[1m-v\033[0m        show version information
{TAB}\033[1m-vd\033[0m       show version number only
{TAB}\033[1m-ast\033[0m      show python ast tree before code
{TAB}\033[1m-f\033[0m        include standard python functions in generated code
{TAB}\033[1m-fn\033[0m       do not include standard python functions in generated code
{TAB}\033[1m-ne\033[0m       do not export functions
{TAB}\033[1m-s\033[0m        generate a require file
{TAB}\033[1m-r\033[0m        use require instead of rbxpy
{TAB}\033[1m-clrtxt\033[0m   modify system shell for a better experience
{TAB}\033[1m-o\033[0m        output file
{TAB}\033[1m-c\033[0m        ignore pyright errors
{TAB}\033[1m-u\033[0m        open this

\033[1mInputs:\033[0m
{TAB}\033[1m-j\033[0m        input is a jupyter notebook
{TAB}\033[1m-b\033[0m        input is bython file
{TAB}\033[1m-py\033[0m       input is python file (default)
{TAB}\033[1m-lua\033[0m      input is lua file to convert to python""")
    sys.exit()

def version():
    print("\033[1;34m" + "copyright:" + "\033[0m" + " roblox-py " + "\033[1m" + VERSION + "\033[0m" + " licensed under the GNU Affero General Public License by " + "\033[1m" + "@AsynchronousAI" + "\033[0m")
    sys.exit(0)

def provideerr(err):
    global proverr
    proverr = err
    
"""The main entry point to the translator"""
def main():
    """Entry point function to the translator"""

    args = sys.argv[1:]
    ast = False
    input_filename = "NONE"
    out = "NONE"
    type = 1 # 1: py->lua, 2: lua->py
    includeSTD = False
    export = True
    skip = False
    reqfile = None
    useRequire = False
    notebook = False
    bython = False
    
    for arg in args:
        if skip:
            skip = False
            continue
        
        if arg == "-v":
            version()
        elif arg == "p":
            error("Plugin is discontinued")
        elif arg == "-vd":
            print(VERSION)
            sys.exit()
        elif arg == "-j":
            notebook = True
        elif arg == "-b":
            bython = True
        elif arg == "-c":
            continue
        elif arg == "-u":
            usage()
        elif arg == "-f":
            includeSTD = True
        elif arg == "-s":
            reqfile = True
        elif arg == "-r":
            useRequire = True
        elif arg == "-fn":
            includeSTD = False
        elif arg == "-ne":
            export = False
        elif arg == "-ast":
            ast = True
        elif arg == "-py":
            type = 1
        elif arg == "-o":
            out = args[args.index(arg)+1]
            skip = True
        elif arg == "-lua":
            type = 2
        elif arg == "-clrtxt":
            # Enable support for ANSI escape sequences
            if os.name == "nt":
                os.system("cmd /c \"setx ENABLE_VIRTUAL_TERMINAL_PROCESSING 1\"")
            else:
                error("Not required on this platform")
            sys.exit(0)
        else:
            if input_filename != "NONE":
                error("Unexpected argument: '{}'".format(arg))
            input_filename = arg
            
    if type == 1:
        if (input_filename == "NONE") and not reqfile:
            usage()
        if (not Path(input_filename).is_file()) and not reqfile:
            error(
                "The given filename ('{}') is not a file.".format(input_filename))

        if not reqfile:
            content = None
            with open(input_filename, "r") as file:
                content = file.read()

            if not content:
                error("The input file is empty.")

        translator = Translator(Config(".robloxpy.json"),
                                show_ast=ast)
        if reqfile:
            reqcode = translator.translate("", True, False, False, True)
            if out != "NONE":
                with open(out, "w") as file:
                    file.write(reqcode)
            else:
                print(reqcode)
            sys.exit(0)
        else:
            if bython:
                try: 
                    from bython import parser #type: ignore
                except:
                    error("bython not installed, please install it with 'pip install bython'")
                parser.parse_file(input_filename, False, '', 'temp')
                print(input_filename)
                with open('temp', 'r') as file:
                    content = file.read()
                    print(content)
                os.remove('temp')
                lua_code = translator.translate(content, includeSTD, False, export, False, useRequire, False)
            elif not notebook:
                pyright = check_pyright()
                if pyright and not "-c" in args:
                    def check():
                        os.environ["PYRIGHT_PYTHON_FORCE_VERSION"] = 'latest'
                        success = subprocess.Popen(["pyright", input_filename]).wait() == 0
                        
                        if not success:
                            print("-----------------------------------------------------")
                            error("compilation failed")
                            sys.exit(1)
                    threading.Thread(target=check).start()
                    
                lua_code = translator.translate(content, includeSTD, False, export, False, useRequire, pyright)
            else:
                nb = json.loads(content)
                cells = nb['cells']
                code = ""
                for i, cell in enumerate(cells):
                    code += '\n\n""" Cell: ' + str(i+1) + ': """ \n\n'
                    if cell['cell_type'] == "code":
                        code += "\n"
                        code += "".join(cell['source'])
                    elif cell['cell_type'] == "markdown":
                        code += '\n""" MD:\n\t' + "\t".join(cell['source']) + '\n"""\n'
                lua_code = translator.translate(code, includeSTD, False, export, False, useRequire, False)
        
        if not ast:
            if out != "NONE":
                with open(out, "w") as file:
                    file.write(lua_code)
            else:
                print(lua_code)
    else:
        error("please use luau2py instead of rbxpy for lua to python conversion.")
        
            
    return 0


if __name__ == "__main__":
    sys.exit(main())
