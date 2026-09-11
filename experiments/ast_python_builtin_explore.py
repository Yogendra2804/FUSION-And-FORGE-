import ast

code = '2 + 3 * (4 + 5)'

tree = ast.parse(code)

print(ast.dump(tree, indent=4))