"""Handles downloading packages from wally."""

import sys, os, json, requests, zipfile
if not (os.path.dirname(os.path.abspath(__file__)).startswith(sys.path[-1])):
    from errormanager import *
else:
    from .errormanager import *

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
  open(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name+".zip"), "x").close()
  with open(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name+".zip"), "wb") as file:
    file.write(response)
  # unzip
  print(info("Unzipping package...", "roblox-pyc wally"))
  with zipfile.ZipFile(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name+".zip"), 'r') as zip_ref:
    zip_ref.extractall(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name))
  # delete the zip
  print(info("Deleting uneeded resources...", "roblox-pyc wally"))
  os.remove(os.path.join(os.getcwd(), "dependencies", "@"+author+"/"+name+".zip"))

