import inspect 

def java(s):
    frame = inspect.currentframe()  
    print(frame.f_locals[f"{str(inspect.signature(java))[1:-1]}"])
    print(frame.f_back.f_locals["arr"])
    return "some Value"


arr = [1 , 2, 3, 4, 5]
java("Collections.sort(arr)")

# print(list(map(str , (inspect.signature(java)).split("\n"))))
string = str(inspect.signature(java))

print(string)

# Did not work as expected, could not get the runtime values of function, 
#   insted, Gave an error. 

# def value_generator():
#     for i in range(10):
#         yield i
# print(inspect.getgeneratorlocals(value_generator))


# day 5-6 of looking for some way to find the runtime values of a function,
#    but could not find any way to do it. Staring to think I'll have to giveup on this.

# Given hint: Use Inspect module and getcurrrentframe()

