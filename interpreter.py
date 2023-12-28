class Token:
    def __init__(self, type_, value=None):
        # Token constructor: Initializes a token with a type and optional value
        self.type = type_
        self.value = value

    def __repr__(self):
        # String representation of the token, used for debugging
        if self.value:
            return f'{self.type}:\"{self.value}\"'
        return f'{self.type}'

    def read(self, obj):
        # Read method for the token
        if self.value:
            if self.type == "TT_NUMBER":
                # Convert the value to a float if it's a number
                self.value = float(self.value)
            return self.value
        else:
            return None

class Interpreter:
    def __init__(self, asts):
        # Interpreter constructor: Initializes the interpreter with a list of Abstract Syntax Trees (ASTs) and an empty storage dictionary
        self.asts = asts
        self.storage = {}

    def execute(self):
        # Execute method: Iterates through each AST and calls its read method with the current Interpreter instance
        for ast in self.asts:
            ast.read(self)

class Node:
    def __init__(self, tok):
        # Node constructor: Initializes a basic node in the parse tree with a token
        self.tok = tok

    def __repr__(self):
        # String representation of the node, used for debugging
        return f'{self.tok.value}'

    def read(self, interpreter):
        # A basic Node does not perform any action when executed
        pass

class BiNode(Node):
    def __init__(self, left_node, op_tok, right_node):
        # BiNode constructor: Initializes a node with binary operation in the parse tree
        super().__init__(op_tok)
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        # String representation of the binary node, used for debugging
        return f'({self.left_node} {self.op_tok.value} {self.right_node})'

    def read(self, interpreter):
        # Perform the binary operation based on the operator type and update the interpreter's storage
        if self.op_tok.type == "TT_PLUS":
            interpreter.storage[self.tok.value] = self.left_node.read(interpreter) + self.right_node.read(interpreter)
        if self.op_tok.type == "TT_MINUS":
            interpreter.storage[self.tok.value] = self.left_node.read(interpreter) - self.right_node.read(interpreter)
        if self.op_tok.type == "TT_DIV":
            interpreter.storage[self.tok.value] = self.left_node.read(interpreter) / self.right_node.read(interpreter)
        if self.op_tok.type == "TT_MULT":
            interpreter.storage[self.tok.value] = self.left_node.read(interpreter) * self.right_node.read(interpreter)
        if self.op_tok.type == "TT_POW":
            interpreter.storage[self.tok.value] = self.left_node.read(interpreter) ** self.right_node.read(interpreter)

class Assign(Node):
    def __init__(self, ident, value):
        # Assignment statement constructor: Initializes an assignment statement node
        super().__init__(ident)
        self.variable = ident.value
        self.value = value

    def __repr__(self):
        # String representation of the assignment statement, used for debugging
        return f"{self.variable} = {self.value}"

    def read(self, interpreter):
        # Execute assignment by updating the variable in the interpreter's storage
        interpreter.storage[self.variable] = self.value.read(interpreter)

class Print(Node):
    def __init__(self, value):
        # Print statement constructor: Initializes a print statement node
        super().__init__(value)

    def __repr__(self):
        # String representation of the print statement, used for debugging
        return f"print({self.tok.value})"

    def read(self, interpreter):
        # Execute print statement by printing the value
        print(self.tok.value.read(interpreter))

class Number(Node):
    def __init__(self, tok):
        # Number constructor: Initializes a numeric value node in the parse tree
        super().__init__(tok)

    def __repr__(self):
        # String representation of the numeric value, used for debugging
        return f'{self.tok.value}'

    def read(self, interpreter):
        # Return the numeric value
        return float(self.tok.value)

class Identifier(Node):
    def __init__(self, tok):
        # Identifier constructor: Initializes a variable node in the parse tree
        super().__init__(tok)

    def __repr__(self):
        # String representation of the variable, used for debugging
        return f'{self.tok.value}'

    def read(self, interpreter):
        # Return the value of the variable from the interpreter's storage
        return interpreter.storage.get(self.tok.value, 0)

# Usage example
if __name__ == "__main__":
    # Example ASTs representing code: x = 5 + 3; print(x)
    token1 = Token("TT_IDENT", "x")
    token2 = Token("TT_NUMBER", "5")
    token3 = Token("TT_PLUS")
    token4 = Token("TT_NUMBER", "3")
    token5 = Token("TT_IDENT", "x")

    ast1 = Assign(Identifier(token1), BiNode(Number(token2), token3, Number(token4)))
    ast2 = Print(Identifier(token5))
    interpreter = Interpreter([ast1, ast2])
    interpreter.execute()
