import ast

code = 'java("Collections.sort(arr)")'

tree = ast.parse(code)

print(ast.dump(tree, indent=4))