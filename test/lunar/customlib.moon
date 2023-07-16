-- Lunar has an extended table library, which is a superset of the standard Lua table library, use table.
-- Lunar also has an extended type system, which is a superset of the standard Lua type system, use type.

checker = type("string", "number", "boolean", "nil", "table", "function")

assert(checker("hello", 1, true, nil, {}, function() end)) -- Matches classes so no errors
assert(checker(1, 2, 3, 4, 5, 6)) -- Doesnt match classes so errors

print table.shuffle({1, 2, 3, 4, 5})

nil -- last line is return value