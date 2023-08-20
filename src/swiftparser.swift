import SwiftSyntax

let source = """
func greet(name: String) {
    print("Hello, \\(name)!")
}
"""

let parser = SyntaxParser()
let syntax = try parser.parse(source: source)

print(syntax)
