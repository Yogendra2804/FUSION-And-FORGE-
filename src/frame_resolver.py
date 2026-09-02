import inspect
import sys
import os

# so it can find lexer.py from the same src/ folder
sys.path.insert(0, os.path.dirname(__file__))
from lexer import tokenization


def java(code):
    frame = inspect.currentframe()
    caller = frame.f_back

    # tokenize the forge code to find every identifier mentioned
    tokens = tokenization(code)

    # collect unique identifiers from the source
    identifiers = set()
    for token in tokens:
        if token[0] == "IDENTIFIER":
            identifiers.add(token[1])

    # check which of those identifiers actually exist in the caller's scope
    # only grab what we actually need, nothing else
    resolved = {}
    for name in identifiers:
        if name in caller.f_locals:
            resolved[name] = caller.f_locals[name]

    # for now just print what we found so we can see it works
    print("Identifiers found in source:", identifiers)
    print("Resolved from caller scope:")
    for name, val in resolved.items():
        print(f"  {name} = {val!r}")

    return resolved


# --- quick demo ---
if __name__ == "__main__":
    arr = [3, 1, 2]
    x = 10
    name = "hello"

    java("""
        Collections.sort(arr);
        arr.add(x);
    """)
