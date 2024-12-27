import sys
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter

class MainInterpreter:
    def __init__(self):
        self.lexer = None
        self.parser = None
        self.interpreter = None
        self.debug_mode = False

    def run(self, code):
        """
        Runs the given code through the lexer, parser, and interpreter.
        """
        try:
            # Lexical Analysis (tokenization)
            print("DEBUG: Starting lexical analysis...")
            self.lexer = Lexer(code)
            tokens = self.lexer.tokenize()
            print(f"DEBUG: Tokenization complete. {len(tokens)} tokens generated.")

            # Parsing the tokens
            print("DEBUG: Starting parsing...")
            self.parser = Parser(tokens)
            ast = self.parser.parse()
            print(f"DEBUG: Parsing complete. AST generated.")

            # Interpreting the AST
            print("DEBUG: Starting interpretation...")
            self.interpreter = Interpreter()
            self.interpreter.interpret(ast)

        except Exception as e:
            print(f"DEBUG: Error during execution: {e}")
            raise e


class Interpreter:
    def __init__(self):
        self.symbol_table = {}

    def interpret(self, ast):
        """
        Interpret the AST and execute the instructions.
        """
        for node in ast:
            if isinstance(node, PrintNode):
                print(node.value)
            elif isinstance(node, FunctionDefNode):
                print(f"Function {node.name} defined.")
            else:
                print(f"Unknown node type: {node}")


class PrintNode:
    def __init__(self, value):
        self.value = value


class FunctionDefNode:
    def __init__(self, name):
        self.name = name


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def parse(self):
        """
        Parse the tokens and generate the Abstract Syntax Tree (AST).
        """
        statements = []
        while self.position < len(self.tokens):
            token = self.tokens[self.position]
            if token['type'] == 'FUNCTION_DEF':
                statements.append(self.parse_function())
            elif token['type'] == 'PRINT':
                statements.append(self.parse_print())
            self.position += 1
        return statements

    def parse_function(self):
        """
        Parse function definitions.
        """
        func_name = self.tokens[self.position + 1]['value']
        self.position += 3  # Move past the function definition
        return FunctionDefNode(func_name)

    def parse_print(self):
        """
        Parse print statements.
        """
        expr = self.tokens[self.position + 1]['value']
        return PrintNode(expr)


class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.position = 0

    def tokenize(self):
        """
        Tokenize the given code.
        """
        while self.position < len(self.code):
            char = self.code[self.position]

            if char.isalpha():
                self.tokens.append(self.parse_keyword())
            elif char == '"':
                self.tokens.append(self.parse_string())
            elif char == ' ' or char == '\n' or char == '\t':
                self.position += 1
            else:
                self.tokens.append(self.parse_symbol())

            self.position += 1
        return self.tokens

    def parse_keyword(self):
        """
        Parse keywords like 'print' or function declarations.
        """
        start = self.position
        while self.position < len(self.code) and self.code[self.position].isalpha():
            self.position += 1
        keyword = self.code[start:self.position]

        if keyword == "print":
            return {'type': 'PRINT', 'value': keyword}
        elif keyword == "function":
            return {'type': 'FUNCTION_DEF', 'value': keyword}
        else:
            return {'type': 'UNKNOWN', 'value': keyword}

    def parse_string(self):
        """
        Parse string literals.
        """
        start = self.position + 1
        self.position += 1
        while self.position < len(self.code) and self.code[self.position] != '"':
            self.position += 1
        string_value = self.code[start:self.position]
        self.position += 1
        return {'type': 'STRING', 'value': string_value}

    def parse_symbol(self):
        """
        Parse symbols (e.g., parentheses, semicolons).
        """
        return {'type': 'SYMBOL', 'value': self.code[self.position]}


def main():
    interpreter = MainInterpreter()

    print("Welcome to Main Language Interpreter.")
    print("Enter code (or 'exit' to quit):")

    while True:
        code = input()
        if code.lower() == 'exit':
            break
        print("DEBUG: Starting lexical analysis...")
        interpreter.run(code)
        print("DEBUG: Concurrent tasks completed.")

if __name__ == "__main__":
    main()
