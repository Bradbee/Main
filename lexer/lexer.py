import re

class Token:
    """
    Represents a token with a type and value.
    """
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token(type='{self.type}', value={self.value})"

class Lexer:
    """
    Converts source code into tokens.
    """
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[self.position]

    def advance(self):
        """
        Move to the next character in the source code.
        """
        self.position += 1
        self.current_char = (
            self.source_code[self.position] if self.position < len(self.source_code) else None
        )

    def peek(self):
        """
        Peek at the next character without advancing.
        """
        next_pos = self.position + 1
        return self.source_code[next_pos] if next_pos < len(self.source_code) else None

    def skip_whitespace(self):
        """
        Skip over whitespace characters.
        """
        while self.current_char and self.current_char.isspace():
            self.advance()

    def skip_comments(self):
        """
        Skip single-line and multi-line comments.
        """
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char and self.current_char != '\n':
                self.advance()
        elif self.current_char == '/' and self.peek() == '*':
            self.advance()
            self.advance()
            while self.current_char and not (self.current_char == '*' and self.peek() == '/'):
                self.advance()
            self.advance()
            self.advance()

    def make_identifier_or_keyword(self):
        """
        Create an identifier or keyword token.
        """
        result = ""
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        keywords = [
            # Variable Declarations
            "let", "const", "var",
            # Control Flow
            "if", "else", "while", "for", "do", "continue", "break", "switch", "case", "default",
            # Functions
            "function", "return", "async", "await", "yield",
            # Classes and Modules
            "class", "extends", "import", "export", "default", "super", "static",
            # Error Handling
            "try", "catch", "throw", "finally",
            # Advanced Features
            "spawn", "join", "detach", "map", "set", "queue", "alloc", "free", "gc", "reflect",
            "proxy", "asm", "type", "interface", "encrypt", "decrypt", "hash", "use strict", 
            "debugger", "delete", "in", "instanceof", "new", "typeof", "with"
        ]
        token_type = "KEYWORD" if result in keywords else "IDENTIFIER"
        return Token(token_type, result)

    def make_number(self):
        """
        Create a number token (integer, float, binary, octal, or hexadecimal).
        """
        result = ""
        if self.current_char == '0' and self.peek() in {'x', 'b', 'o'}:
            base = self.peek()
            result += self.current_char + base
            self.advance()
            self.advance()
            while self.current_char and (
                self.current_char.isdigit() or (base == 'x' and self.current_char in 'abcdefABCDEF')
            ):
                result += self.current_char
                self.advance()
            return Token("NUMBER", int(result, {'x': 16, 'b': 2, 'o': 8}[base]))
        else:
            while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
                result += self.current_char
                self.advance()

            if result.count('.') > 1:
                raise ValueError("Invalid number format")
            return Token("NUMBER", float(result) if '.' in result else int(result))

    def make_string(self):
        """
        Create a string token.
        """
        quote_type = self.current_char
        self.advance()
        result = ""
        while self.current_char and self.current_char != quote_type:
            if self.current_char == '\\':  # Escape sequences
                self.advance()
                if self.current_char:
                    result += self.current_char
            else:
                result += self.current_char
            self.advance()

        if self.current_char != quote_type:
            raise ValueError("Unterminated string literal")
        self.advance()
        return Token("STRING", result)

    def make_operator_or_symbol(self):
        """
        Create a token for operators or symbols.
        """
        symbols = {
            # Arithmetic
            '+', '-', '*', '/', '%', '**',
            # Assignment
            '=', '==', '===', '!=', '!==', '<', '>', '<=', '>=', '+=', '-=', '*=', '/=', '%=', '**=',
            # Logical
            '&&', '||', '!',
            # Increment/Decrement
            '++', '--',
            # Bitwise
            '&', '|', '^', '~', '<<', '>>', '>>>', '&=', '|=', '^=', '<<=', '>>=',
            # Nullish Coalescing
            '??',
            # Optional Chaining
            '?.',
            # Ranges
            '..',
            # Other
            '{', '}', '(', ')', '[', ']', ';', ',', ':', '.', '?', '...', '=>', '|>'
        }

        result = self.current_char
        if self.current_char + self.peek() in symbols or self.current_char + self.peek() + self.peek() in symbols:
            result += self.peek()
            self.advance()
            if self.current_char + self.peek() in symbols:
                result += self.peek()
                self.advance()

        self.advance()
        if result not in symbols:
            raise ValueError(f"Unexpected symbol: {result}")
        return Token("SYMBOL", result)

    def get_next_token(self):
        """
        Get the next token from the source code.
        """
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char == '/' and (self.peek() == '/' or self.peek() == '*'):
                self.skip_comments()
                continue
            if self.current_char.isdigit() or self.current_char == '.':
                return self.make_number()
            if self.current_char.isalpha() or self.current_char == '_':
                return self.make_identifier_or_keyword()
            if self.current_char in {'"', "'"}:
                return self.make_string()
            if self.current_char in {'+', '-', '*', '/', '%', '=', '!', '<', '>', '&', '|', '^', '~', '?', ':', '.', '{', '}', '(', ')', '[', ']', ';', ','}:
                return self.make_operator_or_symbol()

            raise ValueError(f"Unknown character: {self.current_char}")

        return Token("EOF")

    def tokenize(self):
        """
        Tokenize the entire source code.
        """
        tokens = []
        while self.current_char:
            tokens.append(self.get_next_token())
        return tokens
