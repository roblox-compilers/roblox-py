# Floorplan
A plan on how the code will be organize:
- util: Required by all code, provides basic functions
- interface: Core compiler, wrapped by init.cobalt with the API and CLI
- generator: Used by interface to generate code from the ast
- template: Provides a interface to duplicate the template for a inputted extension
- /bridge: provides bridging functions for Lua and Python
- astclass: provides a base class for ast to pyast to generate
- pyast: Uses bridge and uses the python library `ast` to generate a ast and convert it to astclass
- cast: Uses bridge and uses the python library `libclang` to generate a C99 ast and convert it to astclass
- cppast: Uses bridge and uses the python library `libclang` to generate a C++99 (base) ast and convert it to astclass

## AST Reference
```lua
-- variable declarations
local a = 1
local b = "hello"
local c = true

-- if statement
if c then
  print(b)
else
  print("world")
end

-- for loop with index
for i = 1, 5 do
  print(i)
end

-- for loop with table
local t = {1, 2, 3, 4, 5}
for i, v in ipairs(t) do
  print(i, v)
end

-- function definition
function add(x, y)
  return x + y
end

-- function call
local sum = add(a, 2)
print(sum)

-- table indexing
local person = {name = "Alice", age = 30}
print(person.name)

-- table new indexing
local mt = {
  __newindex = function(t, k, v)
    print("setting", k, "to", v)
    rawset(t, k, v)
  end
}
local t = {}
setmetatable(t, mt)
t.foo = "bar"
```

Equal AST:
```bash
- SOURCE
-- DECL A 1 NUMBER
-- DECL B "hello" STRING
-- DECL C true BOOLEAN
-- ASSIGN B "hi" STRING global=true
-- IF C
--- CALL PRINT B
-- ELSE
--- CALL PRINT "world"
-- ENDSTMT
-- FOR I 1 5
--- CALL PRINT I
-- ENDSTMT
-- DECL T {1, 2, 3, 4, 5} TABLE
-- FOR I V T
--- CALL PRINT I V
-- ENDSTMT
-- DECL FUNCTION add X Y
--- RETURN X + Y
-- ENDSTMT
-- DECL SUM add A 2
-- CALL PRINT SUM
-- DECL PERSON {name = "Alice", age = 30} TABLE
-- CALL PRINT PERSON.name
-- DECL MT {}
-- DECL MT __newindex FUNCTION T K V
--- CALL PRINT "setting" K "to" V
--- CALL RAWSET T K V
-- ENDSTMT
-- DECL T {}
-- CALL setmetatable T MT
-- SET T foo "bar"
```
