def ast(code):

    nodes = []
    word = ""

    i = 0

    while i < len(code):

        ch = code[i]

        # Identifier
        if ch.isalnum() or ch == "_":
            word += ch
            i += 1
            continue

        # Finish identifier before special character
        if word:
            nodes.append({
                "type": "identifier",
                "value": word
            })
            word = ""

        # Function call
        if ch == "(":

            # Find matching ')'
            depth = 1
            j = i + 1

            while j < len(code) and depth:
                if code[j] == "(":
                    depth += 1
                elif code[j] == ")":
                    depth -= 1

                j += 1

            inside = code[i + 1:j - 1]

            nodes.append({
                "type": "function_call",
                "arguments": ast(inside)
            })

            i = j
            continue

        # Method / property access
        if ch == ".":

            nodes.append({
                "type": "dot"
            })

            i += 1
            continue

        # Argument separator
        if ch == ",":
            nodes.append({
                "type": "comma"
            })

            i += 1
            continue

        i += 1

    if word:
        nodes.append({
            "type": "identifier",
            "value": word
        })

    return nodes

def print_ast(nodes, indent="", last=True):

    for i, node in enumerate(nodes):

        is_last = i == len(nodes) - 1

        branch = "└── " if is_last else "├── "

        node_type = node["type"]

        if node_type == "identifier":
            print(indent + branch + node["value"])

        elif node_type == "dot":
            print(indent + branch + ".")

        elif node_type == "comma":
            continue

        elif node_type == "function_call":
            print(indent + branch + "FUNCTION_CALL")

            new_indent = indent + ("    " if is_last else "│   ")

            print_ast(
                node["arguments"],
                new_indent
            )

tree = ast(input())

print_ast(tree)