import re

# Define constants for token types
KEYWORDS = {'if', 'else', 'while', 'return', 'print', 'int', 'string', 'bool'}
OPERATORS = {'+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>='}
BRACKETS = {'{', '}', '(', ')', '[', ']', ';'}
LITERALS = {'true', 'false'}

# Define regex patterns for various tokens
TOKEN_PATTERNS = [
    ('NUMBER', r'\d+(\.\d+)?'),  # Integer or Float
    ('HEX_NUMBER', r'0x[0-9A-Fa-f]+'),  # Hexadecimal numbers
    ('STRING', r'"([^"\\]|\\.)*"'),  # Double-quoted strings with escape sequences
    ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'),  # Identifiers (variables, function names)
    ('KEYWORD', r'\b(if|else|while|return|print|int|string|bool)\b'),  # Keywords
    ('OPERATOR', r'(\+|-|\*|\/|\%|\=|\==|\!=|\<|\>|\<=|\>=)'),  # Operators
    ('PUNCTUATION', r'[{}()\[\];,]'),  # Brackets and punctuation
    ('WHITESPACE', r'\s+'),  # Whitespace (spaces, tabs, newlines)
    ('COMMENT', r'//.*'),  # Single-line comments
    ('MULTI_COMMENT', r'/\*.*?\*/'),  # Multi-line comments
    ('ERROR', r'.'),  # Catch all unrecognized characters
]

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.current_pos = 0
        self.line = 1
        self.column = 1
        self._tokenize()

    def _tokenize(self):
        while self.current_pos < len(self.source_code):
            matched = False
            for token_type, pattern in TOKEN_PATTERNS:
                regex = re.compile(pattern)
                match = regex.match(self.source_code, self.current_pos)
                if match:
                    matched = True
                    value = match.group(0)
                    if token_type != 'WHITESPACE' and token_type != 'COMMENT':
                        self.tokens.append((token_type, value))
                    self._advance(len(value))
                    break
            if not matched:
                self._advance(1)  # Skip unrecognized characters and continue

    def _advance(self, length):
        self.current_pos += length
        self.column += length
        if length == 1 and self.source_code[self.current_pos - 1] == '\n':
            self.line += 1
            self.column = 1

    def get_tokens(self):
        return self.tokens

    def _raise_error(self, message):
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {message}")

    def display_tokens(self):
        for token in self.tokens:
            print(f"Token Type: {token[0]}, Value: {token[1]}")

# Example usage:
source_code = """
// This is a comment
int x = 10;
string name = "Main";
if (x > 5) {
    print("X is greater than 5");
} else {
    print("X is not greater than 5");
}
"""

lexer = Lexer(source_code)
lexer.display_tokens()
