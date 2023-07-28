"""Error system for robloxpyc"""
import sys
if 'pip' in sys.modules:
    import colortext, configmanager
else:
    from . import colortext, configmanager
import subprocess, traceback

def candcpperror():
  print(warn("C and C++ are not supported in this build, coming soon! \n\n contributions on github will be greatly appreciated!"))
def error(errormessage, source=""):
  if source != "":
    source = colortext.white(" ("+source+") ")
  if configmanager.getconfig("general", "goofy", False):
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
  if configmanager.getconfig("general", "traceback", False):
    print(colortext.blue("debug ", ["bold"])+infomessage)
    print(traceback.format_exc())
def decreapted(source=""):
    if source != "":
        source = colortext.white(" ("+source+") ")
        print(colortext.yellow("decreapted ", ["bold"])+source+"This feature is decreapted and will be removed in a future version of roblox-pyc")