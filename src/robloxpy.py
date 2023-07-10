import os
from flask import Flask, request
from pyflakes import api
import re
import sys
import typer 

from . import pytranslator, colortext, ctranslator

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
typerapp = typer.Typer() #py
typerapp2 = typer.Typer() #c
typerapp3 = typer.Typer() #cpp
translator = pytranslator.Translator()

def backwordreplace(s, old, new, occurrence):
  li = s.rsplit(old, occurrence)
  return new.join(li)

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
  print(colortext.magenta("roblox-py: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)), "test")+" ...\n Type 'exit' to exit, Press enter to compile."))
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
              if not os.path.exists(relative_path):
                open(relative_path, "x").close()
              with open(relative_path, "w") as f:
                f.write(lua_code)
            except Exception as e:
              print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)))
            

    action = input("")
    if action == "exit":
      exit(0)
    else:
      incli()
  if sys.argv[1] is not None:
    if sys.argv[1] == "p":
      p()
    elif sys.argv[1] == "lib":
      pass
    else:
      incli()
  else:
    incli()

def cw():
  print(colortext.magenta("roblox-c: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)), "test")+" ...\n Type 'exit' to exit, Press enter to compile."))
  def incli():
    # NOTE: Since this isnt packaged yet, using this will only check files inside of the test folder

    # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
    path = os.getcwd()

    for r, d, f in os.walk(path):
      for file in f:
          if '.c' in file:
            # compile the file to a file with the same name and path but .lua
            try:
              ctranslator.translate(os.path.join(r, file))
              print(colortext.green("roblox-c: Compiled "+os.path.join(r, file)))
            except Exception as e:
              print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)))
            

    action = input("")
    if action == "exit":
      exit(0)
    else:
      incli()
  incli()
  
def cpw():
  print(colortext.magenta("roblox-cpp: Ready to compile ", os.path.join(os.path.dirname(os.path.realpath(__file__)), "test")+" ...\n Type 'exit' to exit, Press enter to compile."))
  def incli():
    # NOTE: Since this isnt packaged yet, using this will only check files inside of the test folder

    # Get all the files inside of the path, look for all of them which are .py and even check inside of folders. If this is happening in the same directory as the script, do it in the sub directory test
    path = os.getcwd()

    for r, d, f in os.walk(path):
      for file in f:
          if '.cpp' in file:
            # compile the file to a file with the same name and path but .lua
            try:
              ctranslator.translate(os.path.join(r, file))
              print(colortext.green("roblox-cpp: Compiled "+os.path.join(r, file)))
            except Exception as e:
              print(colortext.red(f"Compile Error for {os.path.join(r, file)}!\n\n "+str(e)))
            

    action = input("")
    if action == "exit":
      exit(0)
    else:
      incli()
  incli()
  
  
if __name__ == "__main__":
  print(colortext.blue("Test mode"))
  mode = input("Select which app to run (1, 2, 3): ")
  
  if mode == "1":
    w()
  elif mode == "2":
    cw()
  elif mode == "3":
    cpw()