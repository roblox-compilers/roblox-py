class Example:
    def __init__(self, name):
        self.name = name

    def print_name(self):
        print(self.name)

    def sethobby(self, hobby):
        self.hobby = hobby

    def printhobby(self):
        print(self.hobby)

    def setage(self, age):
        self.age = age

    def printage(self):
        print(self.age)


new = Example("John")
new.print_name()
new.sethobby("Roblox Game Development")
new.printhobby()