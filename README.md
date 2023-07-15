# Introduction

<div align="center">

<figure><img src=".gitbook/assets/Screenshot 2023-07-10 at 12.06.03 AM.png" alt="" width="375"><figcaption></figcaption></figure>

</div>

## roblox-pyc

[**Docs**](https://robloxpyc.gitbook.io/roblox-pyc) **|** [**Devforum**](https://devforum.roblox.com/t/roblox-py-python-luau/2457105?u=dev98799) **|** [**Github**](https://github.com/AsynchronousAI/roblox.pyc) **|** [**Tests/Examples**](https://github.com/AsynchronousAI/roblox.py/tree/main/test)

***

Python, Lunar, C, C++ Compiler for Roblox.

Python 3.13 (dev), C (all versions), C++ (all versions), Lunar -> Lua(u)

> This has NO RELATION with .pyc files, roblox-py, or roblox-ts

> C/C++ is still in progress.

> Lunar is a language based on MoonScript made for Roblox, at the moment they are identical.

> Python is fully implemented, all code should work because it supports the dev build of Python 3.13.

***
#### Features
- 🔄 Interchangeable </br>
    roblox-pyc supports using Lua, Lunar, roblox-ts, C, C++, and Python all at once so you can have the best of all sides.
- ☄️ Ultrafast compiler </br>
    The roblox-pyc compiler is designed so entire projects can be compiled in a matter of seconds
  
- 📉 Optimized code </br>
  Your code will have near-0 performance drops so you do not have something new to worry about

- ⚠️ Easy error checking </br>
  Your code can easily be checked for errors because of the precompiler error system.
- 📕 All CodeEditors and OS supported </br>
  Since roblox-pyc is a terminal tool based on python it supports all Code Editors and OS, even notepad in windows!
- 🧩 Cross-language module support </br>
  roblox-pyc allows you to require/import modules from other languages.
- 🛠️ Supports all VsCode sync plugins </br>
  Regardless if you use Rojo, Argon, or anything else roblox-pyc is highly customizable and allows you to use any of them
- ↗️ Customizable </br>
  You can customize roblox-pyc to change your C/C++ version or dynamic library or any QoL features, not only that roblox-pyc and all of its dependencies are open-source so you can mod it and change anything to your liking
- 💻 Languages </br>
  roblox-pyc supports a great variety of languages that are fully programmed.
- 🌎 Upload your code to the world </br>
  Using a VScode sync plugin you can upload your code to the world with GitHub, GitLab, whatever.
- 📲  In-roblox plugin </br>
  If you dont what to use VScode, python supports a roblox plugin which can be hosted in the terminal with all the features listed above!
- ❎ Lambda </br>
  Lambda in python is fully supported so you can write full functions in one line
- 🌙 Lunar </br>
  roblox-pyc comes with a custom language called lunar with amazing syntax features which is a modified version of MoonScript for roblox
- 🤖 Use VsCode features </br>
  VsCode has many features including better autofill, linting, and Github Copilot. If you choose to use it roblox-pyc will support it.
  
***
#### Todo:
- Extend py api to support all objects
- Config for ``lib`` to avoid repeating writing file path
- Finish C/C++
- Add types in lunar
- Lunar roblox plugin
***
#### Credits

* [Highlighter](https://github.com/boatbomber/Highlighter). modified to work with python (plugin usage)
* [TextBoxPlus](https://github.com/boatbomber/TextBoxPlus). uses a modified version with autocomplete (plugin usage)
* [pythonlua](https://github.com/dmitrii-eremin/python-lua). this is heavily modified version with flask implementation and compiler changes. (read licenses in [copyright.txt](COPYRIGHTS.txt))
* seasnake. Modified to compile rather than C++-Python but C++-Lua
* MoonScript. Used as a core for Lunar



