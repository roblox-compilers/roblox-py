local checker = type("string", "number", "boolean", "nil", "table", "function")
assert(checker("hello", 1, true, nil, { }))
assert(checker(1, 2, 3, 4, 5, 6))
print(table.shuffle({
  1,
  2,
  3,
  4,
  5
}))
return nil
