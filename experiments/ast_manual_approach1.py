# ex-> java("Collection.sort(arr)")

def ast(code):
    data={}
    word =""
    type = ""
    for idx in range(len(code) - 2):
        ch = code[idx]

        if ch.isalpha():
            word += ch
            continue

        elif ch == '(':
            type = "function"
            

        elif ch== '.':
            type = "method"
            

        elif ch == ',':
            type = "argument"
            

        data[word] = type
        word = ""
    return data

print(ast('java("Collections.sort(arr)")'))
# print("Collections.sort(arr))".strip())