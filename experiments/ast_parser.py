from tokenization_approach3 import tokenization

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ["EOF", ""]

    def consume(self, expected_type=None):
        token = self.current()
        if expected_type and token[0] != expected_type:
            raise Exception(f"Expected {expected_type} but got {token[0]} '{token[1]}'")
        self.pos += 1
        return token

    def parse(self):
        body = []
        # keep going until we hit end of tokens
        while self.current()[0] != "EOF":
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            else:
                self.pos += 1 # just in case to not infinite loop
        return {"type": "Program", "body": body}

    def parse_statement(self):
        # right now just assuming everything is an expression or assignment
        expr = self.parse_expression()
        
        # optional semicolon at the end
        if self.current()[0] == "SEMICOLON":
            self.consume("SEMICOLON")
            
        return {"type": "ExpressionStatement", "expression": expr}

    def parse_expression(self):
        return self.parse_assignment()

    def parse_assignment(self):
        # Assignment is right-associative and lowest precedence
        left = self.parse_logical_or()
        
        # if there is an equal sign it means we are assigning something
        if self.current()[0] == "ASSIGNMENT":
            self.consume("ASSIGNMENT")
            right = self.parse_assignment() # recursive for a = b = 2
            return {"type": "Assignment", "left": left, "right": right}
            
        return left

    def parse_logical_or(self):
        left = self.parse_logical_and()
        
        while self.current()[0] == "OR":
            op = self.consume()
            right = self.parse_logical_and()
            left = {"type": "BinaryExpression", "operator": op[1], "left": left, "right": right}
            
        return left

    def parse_logical_and(self):
        left = self.parse_bitwise()
        
        while self.current()[0] == "AND":
            op = self.consume()
            right = self.parse_bitwise()
            left = {"type": "BinaryExpression", "operator": op[1], "left": left, "right": right}
            
        return left

    def parse_bitwise(self):
        left = self.parse_comparison()
        
        while self.current()[0] == "BINAROP":
            op = self.consume()
            right = self.parse_comparison()
            left = {"type": "BinaryExpression", "operator": op[1], "left": left, "right": right}
            
        return left

    def parse_comparison(self):
        left = self.parse_additive()
        
        while self.current()[0] in ["EQ", "NEQ", "LT", "LTE", "GT", "GTE"]:
            op = self.consume()
            right = self.parse_additive()
            left = {"type": "BinaryExpression", "operator": op[1], "left": left, "right": right}
            
        return left

    def parse_additive(self):
        left = self.parse_multiplicative()
        
        # chaining math operations
        while self.current()[0] in ["PLUS", "MINUS"]:
            op = self.consume()
            right = self.parse_multiplicative()
            left = {"type": "BinaryExpression", "operator": op[1], "left": left, "right": right}
            
        return left

    def parse_multiplicative(self):
        left = self.parse_unary()
        
        while self.current()[0] in ["MULTIPLY", "DIVIDE", "MOD"]:
            op = self.consume()
            right = self.parse_unary()
            left = {"type": "BinaryExpression", "operator": op[1], "left": left, "right": right}
            
        return left

    def parse_unary(self):
        # Unary operators like ! (NOT), - (MINUS), ++, or --
        if self.current()[0] in ["NOT", "MINUS", "INCREMENT", "DECREMENT"]:
            op = self.consume()
            operand = self.parse_unary()
            return {"type": "UnaryExpression", "operator": op[1], "operand": operand}
            
        return self.parse_member_or_call()

    def parse_member_or_call(self):
        # first get the primary thing like 'Collections' or 'arr'
        node = self.parse_primary()
        
        # now keep checking if its followed by a dot or bracket
        # like Collections.sort(arr) -> node is Collections, then we hit DOT
        while self.current()[0] in ["DOT", "LPAREN"]:
            if self.current()[0] == "DOT":
                self.consume("DOT")
                prop = self.consume("IDENTIFIER")
                node = {"type": "MemberAccess", "object": node, "property": prop[1]}
                
            elif self.current()[0] == "LPAREN":
                self.consume("LPAREN")
                args = []
                # parse arguments until we hit the closing bracket
                while self.current()[0] not in ["RPAREN", "EOF"]:
                    args.append(self.parse_expression())
                    if self.current()[0] == "COMMA":
                        self.consume("COMMA")
                self.consume("RPAREN")
                node = {"type": "CallExpression", "callee": node, "arguments": args}
                
        # Check for postfix ++ or --
        if self.current()[0] in ["INCREMENT", "DECREMENT"]:
            op = self.consume()
            node = {"type": "PostfixExpression", "operator": op[1], "operand": node}
            
                
        return node

    def parse_primary(self):
        token = self.current()
        
        if token[0] in ["INT", "FLOAT"]:
            self.consume()
            val = float(token[1]) if token[0] == "FLOAT" else int(token[1])
            return {"type": "Literal", "value": val}
            
        elif token[0] in ["STRING", "CHAR"]:
            self.consume()
            return {"type": "Literal", "value": token[1]}
            
        elif token[0] in ["BOOLEAN TRUE", "BOOLEAN FALSE"]:
            self.consume()
            return {"type": "Literal", "value": (token[0] == "BOOLEAN TRUE")}
            
        elif token[0] == "IDENTIFIER":
            self.consume()
            return {"type": "Identifier", "name": token[1]}
            
        elif token[0] == "LPAREN":
            # handling bracketed math (2+2)
            self.consume("LPAREN")
            expr = self.parse_expression()
            self.consume("RPAREN")
            return expr
            
        else:
            raise Exception(f"idk what to do with this token: {token}")

def build_ast(code):
    tokens = tokenization(code)
    parser = Parser(tokens)
    return parser.parse()

if __name__ == "__main__":
    test_code = "java(x == 10 && x != 5);"
    print("Input:", test_code)
    print("\nAST Tree:")
    import json
    tree = build_ast(test_code)
    print(json.dumps(tree, indent=2))

#  2 + 3 * (4 + 5)