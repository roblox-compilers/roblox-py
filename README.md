# roblox.py
Python compiler for Roblox. 

Python 3.13 (dev) -> Lua(u)
## Dependencies
- ``pip3 install --upgrade pyflakes``
- ``pip3 install flask``
- ``pip3 install pyyaml``

## Credits
- [Highlighter](https://github.com/boatbomber/Highlighter). modified to work with python
- [TextBoxPlus](https://github.com/boatbomber/TextBoxPlus). uses a modified version with autocomplete
- [pythonlua](https://github.com/dmitrii-eremin/python-lua). this is heavily modified version with flask implementation and compiler changes.

  (read licenses in [copyright.txt](/COPYRIGHTS.txt))
## Plugin Guide
### #1 - Clone and start server
```
git clone https://github.com/AsynchronousAI/roblox.py/; cd roblox.py; python3 .
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

## CLI Coming soon

### Learn more
Learn more in the devforum post.
