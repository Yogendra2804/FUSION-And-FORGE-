def tokenization(code):

    KEYWORDS = {
        "int": "INT",
        "float": "FLOAT",
        "double": "DOUBLE",
        "boolean": "BOOLEAN",
        "true": "BOOLEAN TRUE",
        "false": "BOOLEAN FALSE",
        "char": "CHAR",
        "String": "STRING",
        "return": "RETURN",
        "if": "IF",
        "else": "ELSE",
        "while": "WHILE"
    }

    OPERATORS = {
        "!": "NOT",
        "=": "ASSIGNMENT",
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULTIPLY",
        "/": "DIVIDE",
        "%": "MOD",
        "&&": "AND",
        "||": "OR",
        "^": "BINAROP"
    }

    EXTRA = {
        "(": "LPAREN",
        ")": "RPAREN",
        ",": "COMMA",
        ";": "SEMICOLON",
        ".": "DOT"
    }

    tokens = []
    i = 0

    while i < len(code):

        ch = code[i]

        # --------------------------------
        # 1. Ignore whitespace
        # --------------------------------
        if ch.isspace():
            i += 1
            continue

        # --------------------------------
        # 2. String literal
        # --------------------------------
        if ch == '"':
            i += 1
            word = ""

            while i < len(code) and code[i] != '"':
                word += code[i]
                i += 1

            if i >= len(code):
                print("ERROR: Unterminated string")
                return

            i += 1  # skip closing "

            tokens.append(["STRING", word])
            continue

        # --------------------------------
        # 3. Number literal
        # --------------------------------
        if ch.isdigit():

            word = ""

            while i < len(code) and code[i].isdigit():
                word += code[i]
                i += 1

            # Check for FLOAT
            if i < len(code) and code[i] == ".":
                word += "."
                i += 1

                # Decimal part
                while i < len(code) and code[i].isdigit():
                    word += code[i]
                    i += 1

                tokens.append(["FLOAT", word])

            else:
                tokens.append(["INT", word])

            continue

        # --------------------------------
        # 4. Identifier / Keyword
        # --------------------------------
        if ch.isalpha() or ch == "_":

            word = ""

            while (
                i < len(code)
                and (code[i].isalnum() or code[i] == "_")
            ):
                word += code[i]
                i += 1

            if word in KEYWORDS:
                tokens.append([KEYWORDS[word], word])
            else:
                tokens.append(["IDENTIFIER", word])

            continue

        # --------------------------------
        # 5. Two-character operators
        # --------------------------------
        if i + 1 < len(code):

            two_char = code[i:i + 2]

            if two_char in OPERATORS:
                tokens.append([OPERATORS[two_char], two_char])
                i += 2
                continue

        # --------------------------------
        # 6. One-character operators
        # --------------------------------
        if ch in OPERATORS:
            tokens.append([OPERATORS[ch], ch])
            i += 1
            continue

        # --------------------------------
        # 7. Extra symbols
        # --------------------------------
        if ch in EXTRA:
            tokens.append([EXTRA[ch], ch])
            i += 1
            continue

        # --------------------------------
        # 8. Unknown character
        # --------------------------------
        print(f"ERROR: Unknown character '{ch}'")
        i += 1

    # Print tokens
    # for token in tokens:
    #     print(token)

    return tokens


# tokenization(input())
