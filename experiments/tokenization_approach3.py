class TokenizerError(Exception):
    pass

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

    EXTRA = {
        "(": "LPAREN",
        ")": "RPAREN",
        "{": "LBRACE",
        "}": "RBRACE",
        "[": "LBRACKET",
        "]": "RBRACKET",
        ",": "COMMA",
        ";": "SEMICOLON",
        ".": "DOT"
    }

    tokens = []
    i = 0
    line = 1
    col = 1

    def advance(n=1):
        nonlocal i, line, col
        for _ in range(n):
            if i < len(code):
                if code[i] == '\n':
                    line += 1
                    col = 1
                else:
                    col += 1
                i += 1

    while i < len(code):
        ch = code[i]
        current_line = line
        current_col = col

        # 1. Whitespace
        if ch.isspace():
            advance()
            continue

        # 2. Comments
        if ch == '/' and i + 1 < len(code) and code[i+1] == '/':
            # Single line comment //
            advance(2)
            while i < len(code) and code[i] != '\n':
                advance()
            continue
            
        if ch == '/' and i + 1 < len(code) and code[i+1] == '*':
            # Block comment /* ... */
            advance(2)
            closed = False
            while i < len(code):
                if code[i] == '*' and i + 1 < len(code) and code[i+1] == '/':
                    advance(2)
                    closed = True
                    break
                advance()
            if not closed:
                raise TokenizerError(f"Unterminated block comment at line {current_line}, col {current_col}")
            continue

        # 3. String literal
        if ch == '"':
            advance()
            word = ""
            while i < len(code) and code[i] != '"':
                if code[i] == '\\' and i + 1 < len(code):
                    advance() # skip backslash
                    # handle escape sequences
                    esc = code[i]
                    if esc == 'n': word += '\n'
                    elif esc == 't': word += '\t'
                    elif esc == '\\': word += '\\'
                    elif esc == '"': word += '"'
                    else: word += esc
                else:
                    word += code[i]
                advance()
            
            if i >= len(code):
                raise TokenizerError(f"Unterminated string at line {current_line}, col {current_col}")
                
            advance() # skip closing "
            tokens.append(["STRING", word, current_line, current_col])
            continue

        # 4. Character literal
        if ch == "'":
            advance()
            word = ""
            while i < len(code) and code[i] != "'":
                if code[i] == '\\' and i + 1 < len(code):
                    advance()
                    esc = code[i]
                    if esc == 'n': word += '\n'
                    elif esc == 't': word += '\t'
                    elif esc == '\\': word += '\\'
                    elif esc == "'": word += "'"
                    else: word += esc
                else:
                    word += code[i]
                advance()
            
            if i >= len(code):
                raise TokenizerError(f"Unterminated char at line {current_line}, col {current_col}")
            
            if len(word) != 1:
                raise TokenizerError(f"Invalid character literal '{word}' at line {current_line}, col {current_col}")
            
            advance() # skip closing '
            tokens.append(["CHAR", word, current_line, current_col])
            continue

        # 5. Numeric literal
        if ch.isdigit():
            word = ""
            is_float = False
            while i < len(code) and code[i].isdigit():
                word += code[i]
                advance()
                
            # ensure the next char is a digit to not confuse with method call like `1.toString()`
            if i < len(code) and code[i] == ".":
                if i + 1 < len(code) and code[i+1].isdigit():
                    word += "."
                    advance()
                    is_float = True
                    while i < len(code) and code[i].isdigit():
                        word += code[i]
                        advance()
            
            if is_float:
                tokens.append(["FLOAT", word, current_line, current_col])
            else:
                tokens.append(["INT", word, current_line, current_col])
            continue

        # 6. Identifier / Keyword
        if ch.isalpha() or ch == "_":
            word = ""
            while i < len(code) and (code[i].isalnum() or code[i] == "_"):
                word += code[i]
                advance()
                
            if word in KEYWORDS:
                tokens.append([KEYWORDS[word], word, current_line, current_col])
            else:
                tokens.append(["IDENTIFIER", word, current_line, current_col])
            continue

        # 7. Operators (Multi-character & Single-character)
        def match(expected):
            if i + 1 < len(code) and code[i+1] == expected:
                return True
            return False

        if ch == '=':
            if match('='):
                tokens.append(["EQ", "==", current_line, current_col])
                advance(2)
            else:
                tokens.append(["ASSIGNMENT", "=", current_line, current_col])
                advance()
            continue

        if ch == '!':
            if match('='):
                tokens.append(["NEQ", "!=", current_line, current_col])
                advance(2)
            else:
                tokens.append(["NOT", "!", current_line, current_col])
                advance()
            continue

        if ch == '<':
            if match('='):
                tokens.append(["LTE", "<=", current_line, current_col])
                advance(2)
            else:
                tokens.append(["LT", "<", current_line, current_col])
                advance()
            continue

        if ch == '>':
            if match('='):
                tokens.append(["GTE", ">=", current_line, current_col])
                advance(2)
            else:
                tokens.append(["GT", ">", current_line, current_col])
                advance()
            continue
            
        if ch == '+':
            if match('+'):
                tokens.append(["INCREMENT", "++", current_line, current_col])
                advance(2)
            else:
                tokens.append(["PLUS", "+", current_line, current_col])
                advance()
            continue

        if ch == '-':
            if match('-'):
                tokens.append(["DECREMENT", "--", current_line, current_col])
                advance(2)
            else:
                tokens.append(["MINUS", "-", current_line, current_col])
                advance()
            continue
            
        if ch == '&':
            if match('&'):
                tokens.append(["AND", "&&", current_line, current_col])
                advance(2)
            else:
                tokens.append(["BITWISE_AND", "&", current_line, current_col])
                advance()
            continue
            
        if ch == '|':
            if match('|'):
                tokens.append(["OR", "||", current_line, current_col])
                advance(2)
            else:
                tokens.append(["BITWISE_OR", "|", current_line, current_col])
                advance()
            continue

        if ch == '*':
            tokens.append(["MULTIPLY", "*", current_line, current_col])
            advance()
            continue
            
        if ch == '/':
            tokens.append(["DIVIDE", "/", current_line, current_col])
            advance()
            continue
            
        if ch == '%':
            tokens.append(["MOD", "%", current_line, current_col])
            advance()
            continue
            
        if ch == '^':
            tokens.append(["BINAROP", "^", current_line, current_col])
            advance()
            continue

        # 8. Extra symbols
        if ch in EXTRA:
            tokens.append([EXTRA[ch], ch, current_line, current_col])
            advance()
            continue

        # 9. Unknown character
        raise TokenizerError(f"Unknown character '{ch}' at line {current_line}, col {current_col}")

    return tokens

if __name__ == "__main__":
    code1 = '''
    /* This comment never ends
    int x = 10;
    '''
    
    code2 = '''
    char c = 'abcd';
    '''
    
    code3 = "char e = '';"
    
    for code in [code1, code2, code3]:
        print("Testing code:")
        print(code.strip())
        try:
            t = tokenization(code)
            print("Success!")
        except Exception as e:
            print(f"Caught error: {e}\n")
