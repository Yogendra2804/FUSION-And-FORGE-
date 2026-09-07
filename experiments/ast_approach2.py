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
                "inner_code" : ast(code[idx+1:])
            })
            word = ""
            

        elif ch== '.':
            data.append({
                "type": "function",
                "name": word,
                "inner_code" : ast(code[idx+1:])
            })
            word = ""

        elif ch == ',':
            data.append({
                "type": "function",
                "name": word,
                "inner_code" : ast(code[idx+1:])
            })
            word = ""

    return data

print(ast('java("Collections.sort(arr)")'))


# Main problem in this apporach .. not keeping the track of '(' and ')' for causing either
#   recursing limit reach error or faulty siblings being created insted of childs. 