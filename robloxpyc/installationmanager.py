"""Manages updating and installing dependencies"""

# PYPI 
from packaging import version

# FILES
import sys
if 'pip' in sys.modules:
    from errormanager import *
else:
    from .errormanager import * 

# BUILTIN
import subprocess,requests,pkg_resources, os

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
      # Get cfg.pkl 
      script_dir = os.path.dirname(os.path.realpath(__file__))
      returnval = ""
      try:
        with open(os.path.join(script_dir, "cfg.pkl"), "rb") as file:
          returnval = file.read()
      except:
        print(error("Failed to safe-update, data is corrupted. Would you like to force-update, you may lose configuration data.", "auto-updater"))
        choice = input("\t\tDo you want to force-update? (yes/no): ").lower()
        if not choice == "yes":
          sys.exit()
      subprocess.run(["pip", "install", f"roblox-pyc=={latest_version}"])
      with open(os.path.join(script_dir, "cfg.pkl"), "wb") as file:
        file.write(returnval)