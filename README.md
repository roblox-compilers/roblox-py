# roblox.pyc

##### [Docs](https://robloxpydocs.vercel.app) | [Docs (github)](https://github.com/AsynchronousAI/robloxpydocs/tree/main) | [Devforum](https://devforum.roblox.com/t/roblox-py-python-luau/2457105?u=dev98799) | [Github](https://github.com/AsynchronousAI/roblox.py) | [Tests/Examples](https://github.com/AsynchronousAI/roblox.py/tree/main/test)
Python, C, C++ Compiler for Roblox. 

Python 3.13 (dev), C23, C++20 -> Lua(u)

5/103 C/C++ Statements have been implemented 
python 3.13 is fully implemented.
## Changelog:
- Added C, C++ AST (abstract syntax tree), use the cli and it will output AST
- Added automatic variable checking, check which builtin variables are needed
- Added automatic function checking, check which builtin functions are needed
- Reorganized code
- Added more tests
- Cleaned up code
- Did this changelog


## Why did the name get changed to roblox.pyc?
2 reasons:
- It's a python compiler, so it should be named .py**c**
- C, and C++ support.


## Credits
- [Highlighter](https://github.com/boatbomber/Highlighter). modified to work with python
- [TextBoxPlus](https://github.com/boatbomber/TextBoxPlus). uses a modified version with autocomplete
- [pythonlua](https://github.com/dmitrii-eremin/python-lua). this is heavily modified version with flask implementation and compiler changes.
  (read licenses in [copyright.txt](/COPYRIGHTS.txt))
  
# Python:
## Plugin Guide
### #1 - Download and start server
```
pip3 install roblox-pyc
```
```
roblox-py p
```
> Note: This process will end whenever you restart your computer or close the terminal. We recommend using Replit instead.

If any issues occur here report it in github issues.

### #2 - Download client
A download link is in the releases, download the file and place it in your plugins folder. 

You can check where your plugins folder is by:
- opening Roblox Studio
- clicking the Plugins folder icon in the top bar
- and clicking "Plugins Folder"

### #3 Configuring the client
After installing the client open any place, make a new StringValue anywhere named "ROBLOXPY_CONFIG" with its value being the url and then press the roblox.py/Python icon in the plugins tab.

> Note: If you are hosting on a personal computer this step may not be needed because the url is defaulted to localhost:5555

### #4 Open studio and test
Open Roblox Studio, and select any location and click the roblox.py/Python icon in the plugins tab. A window for editing the plugin and a new script named "Script.py" should appear in the explorer.

## CLI
### #1 - Download
```
pip3 install roblox-pyc
```
### #2 - cd to target directory
```
cd Desktop/mygame
```
When called, for every python script roblox-pyc finds it will make a duplicate in the same path with the same name but a .lua ending and with the python code.

### #2 - start
```
roblox-py w
```

# C:
coming soon
# C++:
coming soon

