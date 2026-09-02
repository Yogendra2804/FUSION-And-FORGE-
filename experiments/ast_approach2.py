def ast(code):
    word = ""
    nodes = {}

    i = 0
    while i < len(code):
        ch = code[i]
        if ch.isalpha() or ch == '_':
            word += ch
            continue

        