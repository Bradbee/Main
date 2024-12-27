class Interpreter:
    def __init__(self):
        self.global_scope = {}  # Global scope to store variable values
        self.built_in_functions = {
            'print': self.built_in_print,
            'input': self.built_in_input
        }

    def run(self, ast):
        """
        Main entry point to execute the AST.
        """
        if ast['type'] == 'Program':
            return self.execute_program(ast['body'])
        else:
            raise ValueError("Unsupported AST type")

    def execute_program(self, statements):
        """
        Executes all statements in a program.
        """
        result = None
        for statement in statements:
            result = self.execute_statement(statement)
        return result

    def execute_statement(self, statement):
        """
        Executes a single statement.
        """
        if statement['type'] == 'VariableDeclaration':
            return self.execute_variable_declaration(statement)
        elif statement['type'] == 'ExpressionStatement':
            return self.execute_expression(statement['expression'])
        elif statement['type'] == 'IfStatement':
            return self.execute_if_statement(statement)
        elif statement['type'] == 'FunctionDeclaration':
            return self.execute_function_declaration(statement)
        elif statement['type'] == 'ReturnStatement':
            return self.execute_return(statement)
        else:
            raise ValueError(f"Unknown statement type: {statement['type']}")

    def execute_variable_declaration(self, statement):
        """
        Handles variable declarations and assignments.
        """
        name = statement['name']
        value = self.execute_expression(statement['init'])
        self.global_scope[name] = value
        return value

    def execute_expression(self, expression):
        """
        Evaluates an expression and returns the result.
        """
        if expression['type'] == 'Literal':
            return expression['value']
        elif expression['type'] == 'Identifier':
            return self.global_scope.get(expression['name'], None)
        elif expression['type'] == 'BinaryExpression':
            left = self.execute_expression(expression['left'])
            right = self.execute_expression(expression['right'])
            operator = expression['operator']
            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                return left / right
            elif operator == '==':
                return left == right
            elif operator == '!=':
                return left != right
            elif operator == '>':
                return left > right
            elif operator == '<':
                return left < right
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        elif expression['type'] == 'CallExpression':
            return self.execute_function_call(expression)
        else:
            raise ValueError(f"Unknown expression type: {expression['type']}")

    def execute_if_statement(self, statement):
        """
        Executes an if statement with optional else block.
        """
        condition = self.execute_expression(statement['condition'])
        if condition:
            return self.execute_program(statement['then']['body'])
        elif statement['else']:
            return self.execute_program(statement['else']['body'])
        else:
            return None

    def execute_function_declaration(self, statement):
        """
        Defines a function in the global scope.
        """
        name = statement['name']
        params = statement['params']
        body = statement['body']
        self.global_scope[name] = {'type': 'Function', 'params': params, 'body': body}
        return None

    def execute_function_call(self, expression):
        """
        Executes a function call.
        """
        func_name = expression['callee']
        args = expression['arguments']
        if func_name in self.built_in_functions:
            return self.built_in_functions[func_name](args)
        elif func_name in self.global_scope and self.global_scope[func_name]['type'] == 'Function':
            func = self.global_scope[func_name]
            local_scope = {param: self.execute_expression(arg) for param, arg in zip(func['params'], args)}
            return self.execute_program_with_scope(func['body'], local_scope)
        else:
            raise ValueError(f"Function {func_name} is not defined.")

    def execute_program_with_scope(self, body, local_scope):
        """
        Executes a block of code in a specific local scope (for function calls).
        """
        result = None
        # Save current global scope and switch to the new local scope
        saved_scope = self.global_scope
        self.global_scope = local_scope

        for statement in body:
            result = self.execute_statement(statement)

        # Restore the global scope
        self.global_scope = saved_scope
        return result

    def execute_return(self, statement):
        """
        Handles return statements in functions.
        """
        return self.execute_expression(statement['value'])

    def built_in_print(self, args):
        """
        Print function implementation (built-in).
        """
        for arg in args:
            print(self.execute_expression(arg), end=' ')
        print()  # Print a newline after printing all arguments
        return None

    def built_in_input(self, args):
        """
        Input function implementation (built-in).
        """
        prompt = args[0] if args else ""
        return input(prompt)

