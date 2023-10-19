# v3.27.111 Development Release 1
- Python 3.12
- Use PyRight for type checking
- Syntax slicing
- Fixed empty `except` statements erroring
- is & not is operators
- Fix `\n` or other shorthands in strings being interpreted as actual newlines or what it represents
- Fixed a bug where `x['y'] = 10` will become `local x['y'] = 10`
- `"` in single quote strings are now supported
- All table indexs use `[]` to avoid errors
- Fixed multiline strings not working
- `-->` over `--// \\--` for headers
- `ValueError`, `ImportError`, etc are now supported errors
- Python types are now defined
- Multidemensional array indexing `x[1, 3, 5]`
## Tested
- `pip install table` compiled successfully

# v3.27.111 Development Release 2
- Multiline strings get deconstructed in \n or \t
- Fixed strings that include a \n being interpreted as an actual newline
- Strings will automatically switch from being a single quote to a double quote if it contains a double quote
- Syntax-based slicing now supports missing lower or upper bounds
- Assigning or indexing a variable with a reserved luau keyword will now error
- Support adding lists
- `finally` statements in try/except/finally statements
## Tested
- The entire roblox-py source code itself compiled to Luau successfully