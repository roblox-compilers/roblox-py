<div align="center"><figure><img src=".gitbook/assets/Screenshot 2023-07-10 at 12.06.03 AM.png" alt="" width="375"><figcaption></figcaption></figure></div>

# <div align="center">roblox.pyc </div>

<div align="center"> 
  
  **[Docs](https://robloxpyc.gitbook.io/roblox-pyc) | [Devforum](https://devforum.roblox.com/t/roblox-py-python-luau/2457105?u=dev98799) | [Github](https://github.com/AsynchronousAI/roblox.pyc) | [Tests/Examples](https://github.com/AsynchronousAI/roblox.py/tree/main/test)** </div>


***

Python, C, C++ Compiler for Roblox.

Python 3.13 (dev), C23, C++20 -> Lua(u)

5/103 C/C++ Statements have been implemented python 3.13 is fully implemented.

***



### Credits

* [Highlighter](https://github.com/boatbomber/Highlighter). modified to work with python (plugin usage)
* [TextBoxPlus](https://github.com/boatbomber/TextBoxPlus). uses a modified version with autocomplete (plugin usage)
* [pythonlua](https://github.com/dmitrii-eremin/python-lua). this is heavily modified version with flask implementation and compiler changes. (read licenses in [copyright.txt](COPYRIGHTS.txt))

## Python:

### Plugin Guide

#### #1 - Download and start server

```bash
pip3 install roblox-pyc
```

```bash
roblox-py p
```

> Note: This process will end whenever you restart your computer or close the terminal. We recommend using Replit instead.

If any issues occur here report it in github issues.

#### #2 - Download client

A download link is in the releases, download the file and place it in your plugins folder.

You can check where your plugins folder is by:

* opening Roblox Studio
* clicking the Plugins folder icon in the top bar
* and clicking "Plugins Folder"

#### #3 Configuring the client

After installing the client open any place, make a new StringValue anywhere named "ROBLOXPY\_CONFIG" with its value being the url and then press the roblox.py/Python icon in the plugins tab.

> Note: If you are hosting on a personal computer this step may not be needed because the url is defaulted to localhost:5555

#### #4 Open studio and test

Open Roblox Studio, and select any location and click the roblox.py/Python icon in the plugins tab. A window for editing the plugin and a new script named "Script.py" should appear in the explorer.

### CLI

#### Download

```bash
pip3 install roblox-pyc
```

#### Open Directory

```bash
cd Desktop/mygame
```

When called, for every python script roblox-pyc finds it will make a duplicate in the same path with the same name but a .lua ending and with the python code.



#### Install library

This is how you would install a library:

```
roblox-py lib shared/roblox-pyc.lua
```

```
roblox-{type} lib {path}.lua
```

#### Compile files:

If you need to you can run

```
roblox-py c
```

```
roblox-c c
```

```
roblox-cpp c
```

to find all code in lua, delete it and add a file with the same name but of the desired language&#x20;

> This does not compile code, it will return a empty file with the old script as a comment, this is used to convert default Rojo worlds into your desired language.

#### Start

Simply click enter after running one of the following commands and it will recompile all scripts.

#### Python:

```
roblox-py w
```

#### C:

```
roblox-c w
```

#### C++

```
roblox-cpp w
```
