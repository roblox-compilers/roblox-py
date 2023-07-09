"""
XL.py (Stands for Extralarge)

A test script for the Roblox.py compiler that uses all of the python 3.13 features.
"""

# Imports
import x as y

SSS = py.services.ServerScriptService

for i in range(10):
    print(i)
    
while True:
    print("This is an infinite loop")
    break

with open("test.txt", "w") as f:
    f.write("This is a test file")
    
def test():
    print("This is a function, ran inside of the async function")
    
async def async_test():
    print("This is an async function")
    await test()
    
async_test()

data = {
    "test": "This is a test"
}

for i in data:
    print(i)
    
class Test:
    def __init__(self):
        print("This is a class")
        
    def test(self):
        print("This is a class method")
        
    @staticmethod
    def static_test():
        print("This is a static method")
        
    @classmethod
    def class_test(cls):
        print("This is a class method")
    
new_test = Test()
new_test.test()
new_test.static_test()
new_test.class_test()

string = "This"
string2 = "This is a test string"
if string1 not in string2:
    print("x is not in y")
else:
    print("x is in y")