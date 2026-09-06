# def ast(code):
#     word = ""
#     nodes = {}

#     i = 0
#     while i < len(code):
#         ch = code[i]
#         if ch.isalpha() or ch == '_':
#             word += ch
#             continue

# ex-> java("Collection.sort(arr)")

def ast(code):
    data=[]
    word =""
    for idx in range(len(code)):
        ch = code[idx]

        if ch.isalpha():
            word += ch
            continue

        elif ch == '(':
            data.append({
                "type": "function",
                "name": word,
                "inner_code" : code[idx:]
            })
            word = ""
            

        elif ch== '.':
            data.append({
                "type": "function",
                "name": word,
                "inner_code" : code[idx:]
            })
            word = ""

        elif ch == ',':
            data.append({
                "type": "function",
                "name": word,
                "inner_code" : code[idx:]
            })
            word = ""

    return data

print(ast('java("Collections.sort(arr)")'))