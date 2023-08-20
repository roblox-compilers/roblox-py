import pyflakes.api as api
import requests
from flask import Flask, request
import sys
import os 
if not (os.path.dirname(os.path.abspath(__file__)).startswith(sys.path[-1])):
    from reporter import Reporter
    import pytranslator
else:
    from .reporter import Reporter
    from . import pytranslator

def p():
  app = Flask(__name__)
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