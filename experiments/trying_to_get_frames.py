import inspect
from Tokenization_Apporach2 import tokenization
def get_frames(code):
    string = inspect.currentframe()
    caller = string.f_back

    # Here I need to extract all the local values and check if their corossponding value 
    # exist or not if yes then print if no then move forward. 
    # 

    get_current_frame_locals = string.f_locals[f"{str(inspect.signature(get_frames))[1:-1]}"]     

    # Here I need to fet all the identifiers from the input code and then iterate over them
    # To check for corossponding values. 

    tokens = tokenization(get_current_frame_locals)
    IDENTIFIERS_set = set()
    arr_value = caller.f_locals["arr"]

    # print(get_current_frame_locals)

    for token in tokens:
        if token[0] == "IDENTIFIER":
            IDENTIFIERS_set.add(token[1])

    for val in IDENTIFIERS_set:
        try:
            print(caller.f_locals[val])
        except:
            continue

    # return arr_value
    # print(IDENTIFIERS_set)

arr = [3, 1, 2]

get_frames("""
    Collections.sort(arr);
""")

# print(result)