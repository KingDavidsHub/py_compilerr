from lexer import Lexer
from parser_1 import Parser, Token
from interpreter import Interpreter, Node, BiNode, Assign, Print, Number, Identifier
from debugger import Debugger
from validator import validate
import sys

def main():
    # Get the source code file path from command line arguments
    source = sys.argv[1]

    # Create a new lexer instance with the provided source code
    new_lexer = Lexer(source)

    # Get tokens from the lexer
    tokens = new_lexer.getTokens()

    # Create a new parser instance with the obtained tokens
    new_parser = Parser(tokens)

    # Generate Abstract Syntax Trees (ASTs) using the parser
    asts = new_parser.runParse()

    # Create a new interpreter instance with the generated ASTs
    new_interpreter = Interpreter(asts)

    # Execute the interpreter to interpret and run the program
    new_interpreter.execute()

    # Enter the user command loop of the debugger
    debugger = Debugger()
    debugger.user_command_loop()

    # Check if previously identified errors have been fixed
    validate(source)

# Call the main function when the script is executed
if __name__ == "__main__":
    main()
