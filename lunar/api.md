---
description: How can you use the built in API.
---

# API

Lunar includes all of the built-in functions as MoonScript (in a future version we may change the core to YueScript for more), and more type and class-related functions.

## Types

(check [introduction.md](../cli-docs/introduction.md "mention") for all credits, `t` will have the full docs of types)

```moonscript
-- Use the built-in type library
newCheck = type.tuple(type.string, type.optional(type.number))
string = type.optional(t.string)
unioned = type.union(type.number, type.nan)

-- Test tuple checkers
assert(newCheck("A")) -- Works!
assert(newCheck("A", 1)) -- Works!
assert(newCheck(1)) -- Errors!

-- Test single checkers
print(type.string("Am I string?")) -- true
print(type.string(nil)) -- false, <errormessage>
print(unioned(5)) -- true: it is a number or NaN



nil -- add nil to the end of the file as the return value for the compiled code
```

***

## Tables

(check [introduction.md](../cli-docs/introduction.md "mention") for all credits)

#### `table.count`

Returns the total number of the element in a table.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: number

**Example**

```moonscript
print(table.count({'bunch', 'of', 'strings'})) --> 3
```

#### `table.deepCount`

Returns the total number of the element in a table recursively.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: number

**Example**

```moonscript
print(table.deepCount({'bunch', 'of', 'string', {'and', 'even', 'more', 'string'}})) --> 7
```

#### `table.includes`

Determines whether the table contains the passed `value`, returning `true` or `false` as appropriate.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |
| value     | any   |

Returns: boolean

**Example**

```moonscript
print(table.includes({'Bob', 'Jeff', 'Andrew'}, 'Andrew')) --> true
```

#### `table.has`

Determines if the table has `index` on it, returning `true` or `false` as appropriate.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |
| index     | any   |

Returns: boolean

**Example**

```moonscript
t = {
    data = {
        value = 0,
        info = 'cool'
    },
    users = {
        '878973176219', '7287643892364'
    }
}
print(table.has(t, 'data')) --> true
```

#### `table.isEmpty`

Determines if the table is not empty. Returns `true` or `false`, as appropriate.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: boolean

**Example**

```moonscript
print(table.isEmpty({})) --> true
print(table.isEmpty({2, 3, 0, 1})) --> false
```

#### `table.isArray`

Determines if the table is a array-like table.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: boolean

**Example**

```moonscript
print(table.isArray({1, 2, 3})) --> true
print(table.isArray({something = 'Rick'})) --> false
```

#### `table.isDictionary`

Determines if the table is a dictionary-like table. A dictionary is defined as a table containing keys that are not positive integers. (e.g. `{ [19] = 'random text', debug = true }`)

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: boolean

**Example**

```moonscript
print(table.isDictionary({1, 9, 8, 7})) --> false
print(table.isDictionary({something = 'Astley'})) --> true
```

#### `table.copy`

Returns a new copy of the table, one layer deep.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: table

**Example**

```moonscript
original = {'Itadori Yuuji', 'Nobara Kugisaki'}
duplicate = table.copy(original)
table.insert(duplicate, 'Ryomen Sukuna')
print(duplicate) --> {'Itadori Yuuji', 'Nobara Kugisaki', 'Ryomen Sukuna'}
```

#### `table.deepCopy`

Returns a copy of table, recursively. If a table is encountered, it is recursively deep-copied. Metatables are not copied.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: table

**Example**

```moonscript
data = {
    Cash = 69,
    Gems = 420,
    Inventory = {
        'very cool item #1',
        'very cool item #2'
    }
}
duplicate = table.deepCopy(data)
duplicate.Cash = 100
duplicate.Gems = 500
table.insert(data.Inventory, 'epic item')

print(duplicate) --> { Cash = 100, Gems = 500, Inventory = { 'very cool item #1', 'very cool item #1', 'epic item' } }
```

#### `table.reverse`

Reverses the element of an array-like table in place.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: nil

**Example**

```moonscript
array = {1, 2, 3, 4, 5}
table.reverse(array)
print(array) --> {5, 4, 3, 2, 1}
```

#### `table.reversed`

Returns a copy of an array-like table with its element in reverse order. The original remains unchanged.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: nil

**Example**

```moonscript
array = {1, 2, 3, 4, 5}
reversed = table.reversed(array)
print(reversed) --> {5, 4, 3, 2, 1}
```

#### `table.keys`

Returns a new array-like table where all of its values are the keys of the original table.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: table

**Example**

```moonscript
dict = {
    Player1 = {10, 300, 40},
    Player2 = {50, 1000, 30},
}
print(table.keys(dict)) --> {'Player1', 'Player2'}
```

#### `table.values`

Returns a new array-like table where all of its values are the values of the original table.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: table

**Example**

```moonscript
dict = {
    Player1 = {10, 300, 40},
    Player2 = {50, 1000, 30},
}
print(table.values(dict)) --> {{10, 300, 40}, {50, 1000, 30}}
```

#### `table.randomIpair`

Returns a random (index, value) pair from an array-like table.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: number, any

**Example**

```moonscript
array = {'Samsung', 'ASUS', 'Lenovo', 'HP'}
print(table.randomIpair(array)) --> 2    ASUS
```

#### `table.randomPair`

Returns a random (key, value) pair from a table.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: any, any

**Example**

```moonscript
dict = {
    Player1 = 'John Wick',
    Player2 = 'Joe Mama',
    Player3 = 'Peter Griffin',
    Player4 = 'Barry',
}
print(table.randomPair(array)) --> Player3    Peter Griffin
```

#### `table.sorted`

Returns a copy of an array-like table sorted using Lua's `table.sort`.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: table

**Example**

```moonscript
rates = {1, 3, 2, 6, 4, 5, 7, 5, 3}
sorted = table.sorted(rates, function(a, b) return a < b end)
print(sorted) --> {1, 2, 3, 3, 4, 5, 5, 6, 7}
```

#### `table.slice`

Returns a new array-table that is a slice of the original, defined by the start and stop bounds and the step size. Default start, stop, and step values are 1, #tbl, and 1 respectively.

**Parameters**

| parameter | type   | optional |
| --------- | ------ | -------- |
| tbl       | table  |          |
| start     | number | ✔️       |
| stop      | number | ✔️       |
| step      | number | ✔️       |

Returns: table

**Example**

```moonscript
strings = {'when', 'the', 'imposter', 'is', 'sus'}
duplicate = table.slice(strings, 1, 5, 2)
print(duplicate) --> {'when', 'imposter', 'sus'}
```

#### `table.findValue`

Iterates through a table until a value satisfies the test function. The `value` is returned if one of the value satisfies the test function. Otherwise, `nil` is returned.

**Parameters**

| parameter | type     |
| --------- | -------- |
| tbl       | table    |
| testFn    | function |

**testFn parameters**

| parameter | type | optional |
| --------- | ---- | -------- |
| value     | any  |          |
| key       | any  | ✔️       |

Returns: any

**Example**

```moonscript
strings = {'when', 'the', 'imposter', 'is', 'sus'}
testFn = function(str) return #str > 5
print(table.findValue(strings, testFn)) --> 'imposter'
```

#### `table.findIndex`

Iterates through a table until a index satisfies the test function. The `key` is returned if one of the index satisfies the test function. Otherwise, `nil` is returned.

**Parameters**

| parameter | type     |
| --------- | -------- |
| tbl       | table    |
| testFn    | function |

**testFn parameters**

| parameter | type | optional |
| --------- | ---- | -------- |
| value     | any  |          |
| key       | any  | ✔️       |

Returns: any

**Example**

```moonscript
strings = {'when', 'the', 'imposter', 'is', 'sus'}
testFn (str)->
    return #str
index = table.findIndex(strings, testFn)
print(index) --> 3
print(strings[index]) --> imposter
```

#### `table.filter`

Returns a new table containing all elements of the calling table for which provided filtering function returns `true`.

**Parameters**

| parameter | type     |
| --------- | -------- |
| tbl       | table    |
| filterFn  | function |

**filterFn parameters**

| parameter | type | optional |
| --------- | ---- | -------- |
| value     | any  |          |
| key       | any  | ✔️       |

Returns: table

**Example**

```moonscript
scores = {Paul = 75, John = 70, Walker = 90, Bruce = 70, Clark = 69, Stark = 100, Steve = 85}
filter = (score) ->
   return score >= 80

print(table.filter(scores, filter)) --> {Walker = 90, Stark = 100, Steve = 85}
```

#### `table.map`

Returns a new table containing the results of calling a function on every element in this table.

**Parameters**

| parameter | type     |
| --------- | -------- |
| tbl       | table    |
| mapFn     | function |

**mapFn parameters**

| parameter | type | optional |
| --------- | ---- | -------- |
| value     | any  |          |
| key       | any  | ✔️       |

Returns: table

**Example**

```moonscript
-- No docs yet ):
```

#### `table.every`

Iterates through the table and run the test function to to every element to check if it satisfies the check. If all elements satisfies the check, it returns `true`. Otherwise it returns `false`.

**Parameters**

| parameter | type     |
| --------- | -------- |
| tbl       | table    |
| testFn    | function |

**testFn parameters**

| parameter | type | optional |
| --------- | ---- | -------- |
| value     | any  |          |
| key       | any  | ✔️       |

Returns: boolean

**Example**

```moonscript
array = {'John', 'Paul', 'Bob', 'Walker', 'Steve', 'Alex'}
str = (score) ->
   return type(str) == 'string'

print(table.every(array, strCheck)) --> true
```

#### `table.merge`

Returns a new table that is the table joined with other table(s).

**Parameters**

| parameter | type  |
| --------- | ----- |
| ...tbl    | table |

Returns: table

**Example**

```moonscript
team_A= {'John', 'Paul', 'Bob'}
team_B = {'Walker', 'Steve', 'Alex'}
all_players = table.merge(team_A, team_B)
print(all_players) --> {'John', 'Paul', 'Bob', 'Walker', 'Steve', 'Alex'}
```

#### `table.fill`

Changes all elements in an array-like table to a static value from start index (default: `1`) to an end index (default: `#tbl`). It returns the modified array-like table.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: table

**Example**

```moonscript
print(table.fill({1, 2, 3, 4, 5, 6}, 0)) --> {0, 0, 0, 0, 0, 0}
print(table.fill({1, 2, 3, 4, 5, 6}, 6, 1, 3)) --> {1, 6, 6, 4, 5, 6}
print(table.fill({1, 2, 3, 4, 5, 6}, 69, 2, 5)) --> {1, 69, 69, 69, 69, 6}
```

#### `table.removeDupes`

Returns a new copy of the original array-like table and removes duplicate elements that exists on that table.

**Parameters**

| parameter | type  |
| --------- | ----- |
| tbl       | table |

Returns: table

**Example**

```moonscript
messy_array = {1, 1, 2, 3, 5, 5, 4, 'A', 'A', 'B', 'C', 'A', 'B', 'A'}
clean_array = table.removeDupes(messyArray)
print(clean_array) --> {1, 2, 3, 5, 4, 'A', 'B', 'C'}
```
