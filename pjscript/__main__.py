from .interpreter import Lexer, Parser, Interpreter
import sys


def print_tok(lexer, callback=None):
    for idx, token in enumerate(lexer):
        print(idx, token)
        if callback:
            callback(token)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            source_code = f.read()
            lexer = Lexer(source_code)
            parser = Parser(lexer)
            tree = parser.parse()
            interpreter = Interpreter(tree)
            interpreter.interpret()

    if len(sys.argv) == 3:
        with open(sys.argv[2], "r") as f:
            source_code = f.read()
            lexer = Lexer(source_code)
            parser = Parser(lexer)
            # THIS WILL SHOW YOU THE TOKENS
            if sys.argv[1] == "-L":
                print_tok(lexer)

            # THIS WILL SHOW YOU TOP LEVE OF TREE
            elif sys.argv[1] == "-A":
                for node in parser.parse().body:
                    print(node)
            else:
                print("UNKOWN CAMMAND!")
