from flask import Flask, request
from pythonlua.translator import Translator

import sys
import pylint



from io import StringIO

from pylint.lint import Run
from pylint.reporters.text import TextReporter

app = Flask(__name__)
pylint_output = StringIO()
reporter = TextReporter(pylint_output)

def check(source):
  with open("debug.py", 'w') as file:
    file.write(source)
    Run(["debug.py"], reporter=reporter, exit=False)
    return (pylint_output.getvalue())

@app.route('/', methods=["GET", "POST"]) 
def base_page():
  code = (request.data).decode()

  translator = Translator()
  try:
    lua_code = translator.translate(code)
  except Exception as e:
    return "CompileError!:"+str(e)

  return lua_code

@app.route('/debug', methods=["GET", "POST"]) 
def debug():
  code = (request.data).decode()

  return check(code)

app.run(
 host='0.0.0.0', 
 port=5555 
)

