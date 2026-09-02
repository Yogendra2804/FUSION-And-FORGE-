# Collections.sort(arr)
'''
Eventually we need to distinguish:

arr  → Identifier
10   → Integer literal
10.5 → Float literal
"hi" → String literal
true → Boolean

'''

def tokenization(code):
    # keywords = ["int" , "float" , "double" , "boolean" , "char" , "String" , "return" , "if" ,"else" , "while" , "for" , "new"]

    KEYWORDS = {
    "int" : "INT",
    "float" : "FLOAT",
    "double" : "DOUBLE",
    "boolean" : "BOOLEAN",
    "true" : "BOOLEAN TRUE",
    "false" : "BOOLEAN FALSE",
    "char" : "CHAR",
    "String" : "STRING",
    "return" : "RETURN",
    "if" : "IF",
    "else" : "ELSE",
    "while" : "WHILE"
    }

    OPERATORS = {
        "!" : "NOT" ,
        "=" : "ASSIMENT" ,
        "+" : "PLUSE" ,
        "-" : "MINUS" , 
        "*" : "MULTIPLY" ,
        "/" : "DIVIDE" ,
        "%" : "MOD" , 
        "&&" : "AND" ,
        "||" : "OR" ,
        "^" : "BINAROP" 
    }

    EXTRA = {
        "(" : "RParan" ,
        ")" : "LParan" ,
        "," : "COMMA" ,
        ";" : "SEMICOLAN" ,
        "." : "DOT"
    }
    list = [] 
    word = ""
    if code.isdigit() : list.append(["INT", f"{code}"]) ; 

    elif '.' in code and code.replace('.', '', 1).isdigit():
        list.append(["FLOAT", f"{code}"])

    elif code in KEYWORDS : list.append([KEYWORDS[code] , f"{code}"])

    elif code.startswith('"') and code.endswith('"') : list.append(["STRING" , f"{code}"]) ; 
    
    else: 
        stringcheck = False
        count= 0
        for idx in range(len(code)):
            ch = code[idx]
            # if ch.isalpha() and  not code[idx+1].isalpha(): list.append(["IDENTIFIER" , f"{ch}"]);
            if ch in OPERATORS: list.append([OPERATORS[ch] , f"{ch}"])
            if ch == " ": 
                if word in KEYWORDS : 
                    list.append([KEYWORDS[word] , f"{word}"])

                elif word in OPERATORS: list.append([OPERATORS[word] , f"{word}"])
                
                else: list.append(["IDENTIFIER" , f"{word}"]);

                word = "" 
                continue
            if ch.isalnum() or ch == '_':
                word += ch

                # if len(word) == len(code) : list.append(["IDENTIFIER" , f"{word}"])
                if '.' in word and word.replace('.', '', 1).isdigit():
                    list.append(["FLOAT", f"{word}"])

                elif word.isdigit() and idx+1 == len(code): list.append(["INT" , f"{word}"])
                
                if word.isalpha() and idx+1 == len(code): list.append(["Identifier" , f"{word}"])

                continue
            
            else:
                
                if '_' in word: list.append(["IDENTIFIER" , f"{word}"])

                if ch == '"' : 
                    stringcheck = True
                    count += 1

                    if count == 2 and word != "":
                        list.append(["STRING" , f"{word}"])
                        count = 0
                        stringcheck = False
                        word = ""
                    continue

                if stringcheck: word += ch ; continue



                if ch == '.' and (code[idx+1]).isdigit():
                    word += '.'
                    continue

                if '.' in word and word.replace('.', '', 1).isdigit():
                    list.append(["FLOAT", f"{word}"])

                elif word.isdigit():
                    list.append(["INT", f"{word}"])

                elif word.isalpha(): list.append(["IDENTIFIER",f"{word}"])

                if ch in EXTRA:
                    list.append([EXTRA[ch] ,f"{ch}"])
                
                else:
                    word += ch
                    continue
                    # list.append(["IDENTIFIER" , f"{ch}"])
                
            if word : word = ""


    for lis in list:print(lis)

# tokenization("Collections.sort(arr , x , 10 , 99.5)")
# print("\n\n")
# tokenization("method(a, getValue(x, y), c)")

tokenization(input())
