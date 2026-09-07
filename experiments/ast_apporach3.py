def ast(code):
    data = []
    stack = []

    word = ""
    current = None

    i = 0

    while i < len(code):
        ch = code[i]

        # -------------------------
        # Read a name
        # -------------------------
        if ch.isalpha() or ch == '_':
            word += ch

        # -------------------------
        # Member access "."
        # -------------------------
        elif ch == '.':
            if word:
                node = {
                    "type": "method",
                    "name": word,
                    "inner_code": []
                }

                if current is None:
                    data.append(node)
                else:
                    current["inner_code"].append(node)

                current = node
                word = ""

        # -------------------------
        # Function call "("
        # -------------------------
        elif ch == '(':
            if word:
                node = {
                    "type": "function",
                    "name": word,
                    "inner_code": []
                }

                if current is None:
                    data.append(node)
                else:
                    current["inner_code"].append(node)

                current = node
                word = ""

            # Save current node so we know where
            # to return after this function call.
            stack.append(current)

        # -------------------------
        # End function call ")"
        # -------------------------
        elif ch == ')':

            if not stack:
                print("Error: Unmatched closing parenthesis")
                return data

            # Finish the current scope
            current = stack.pop()

        # -------------------------
        # Argument ","
        # -------------------------
        elif ch == ',':
            if word:
                node = {
                    "type": "argument",
                    "name": word,
                    "inner_code": []
                }

                if current is None:
                    data.append(node)
                else:
                    current["inner_code"].append(node)

                word = ""

        i += 1

    # Handle final word
    if word:
        node = {
            "type": "argument",
            "name": word,
            "inner_code": []
        }

        if current is None:
            data.append(node)
        else:
            current["inner_code"].append(node)

    if stack:
        print("Error: Unmatched opening parenthesis")

    return data

result = ast("java(Collections.sort(arr))")

print(result)