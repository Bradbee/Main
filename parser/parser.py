import re
from error.errors import SyntaxError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # List of tokens from the lexer
        self.current = 0      # Pointer to the current token in the list

    def parse(self):
        """
        Main entry point for the parser. This method will start parsing the tokens and build the AST.
        """
        try:
            ast = self.program()
            if not self.is_at_end():
                raise SyntaxError("Unexpected input after program end.")
            return ast
        except SyntaxError as e:
            print(f"Syntax Error: {e}")
            return None

    def program(self):
        """
        A program consists of one or more statements.
        """
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())
        return {'type': 'Program', 'body': statements}

    def statement(self):
        """
        A statement can either be a variable declaration, expression, or control structure.
        """
        if self.match('KEYWORD', 'int', 'float', 'string'):
            return self.variable_declaration()
        elif self.match('KEYWORD', 'if'):
            return self.if_statement()
        else:
            return self.expression_statement()

    def expression_statement(self):
        """
        An expression followed by a semicolon.
        """
        expr = self.expression()
        self.consume('PUNCTUATION', ';', "Expect ';' after expression.")
        return {'type': 'ExpressionStatement', 'expression': expr}

    def expression(self):
        """
        An expression can be a variety of operations. For simplicity, this handles basic operators.
        """
        left = self.term()
        while self.match('OPERATOR', '+', '-'):
            operator = self.previous()
            right = self.term()
            left = {'type': 'BinaryExpression', 'left': left, 'operator': operator, 'right': right}
        return left

    def term(self):
        """
        A term is either a number, an identifier, or a grouped expression.
        """
        if self.match('NUMBER'):
            return {'type': 'Literal', 'value': self.previous()['value']}
        elif self.match('ID'):
            return {'type': 'Identifier', 'name': self.previous()['value']}
        elif self.match('PUNCTUATION', '('):
            expr = self.expression()
            self.consume('PUNCTUATION', ')', "Expect ')' after expression.")
            return expr
        else:
            raise SyntaxError("Expected expression.")

    def variable_declaration(self):
        """
        A variable declaration, like 'int x = 10;'
        """
        type_token = self.consume('KEYWORD', "int", "float", "string", "Expect a type.")
        var_name = self.consume('ID', "Expect variable name.")
        self.consume('OPERATOR', '=', "Expect '=' after variable name.")
        value = self.expression()
        self.consume('PUNCTUATION', ';', "Expect ';' after variable declaration.")
        return {'type': 'VariableDeclaration', 'name': var_name['value'], 'init': value}

    def if_statement(self):
        """
        A simple 'if' statement.
        """
        self.consume('PUNCTUATION', '(', "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume('PUNCTUATION', ')', "Expect ')' after if condition.")
        self.consume('PUNCTUATION', '{', "Expect '{' after if condition.")
        then_block = self.block()
        else_block = None
        if self.match('KEYWORD', 'else'):
            self.consume('PUNCTUATION', '{', "Expect '{' after 'else'.")
            else_block = self.block()
        return {
            'type': 'IfStatement',
            'condition': condition,
            'then': then_block,
            'else': else_block
        }

    def block(self):
        """
        A block is a list of statements enclosed in curly braces.
        """
        statements = []
        while not self.check('PUNCTUATION', '}') and not self.is_at_end():
            statements.append(self.statement())
        self.consume('PUNCTUATION', '}', "Expect '}' after block.")
        return {'type': 'Block', 'body': statements}

    def match(self, *types):
        """
        Checks if the current token matches any of the provided token types.
        """
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False

    def check(self, type):
        """
        Checks if the current token matches the given type.
        """
        if self.is_at_end():
            return False
        return self.peek()['type'] == type

    def consume(self, type, value=None, error_message=None):
        """
        Consumes a token if it matches the type. Throws a SyntaxError otherwise.
        """
        if self.check(type) and (value is None or self.peek()['value'] == value):
            return self.advance()
        if error_message:
            raise SyntaxError(error_message)
        raise SyntaxError(f"Expected {type}, but found {self.peek()['type']}.")

    def advance(self):
        """
        Moves the current pointer to the next token.
        """
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self):
        """
        Returns the previous token.
        """
        return self.tokens[self.current - 1]

    def peek(self):
        """
        Returns the current token without advancing the pointer.
        """
        return self.tokens[self.current]

    def is_at_end(self):
        """
        Checks if the end of the token list has been reached.
        """
        return self.peek()['type'] == 'EOF'


