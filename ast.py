class ASTNode:
    def __init__(self, node_type, **kwargs):
        self.type = node_type
        for key, value in kwargs.items():
            setattr(self, key, value)


# Utility functions for creating AST nodes

def create_program(statements):
    return ASTNode('Program', body=statements)

def create_variable_declaration(name, init):
    return ASTNode('VariableDeclaration', name=name, init=init)

def create_identifier(name):
    return ASTNode('Identifier', name=name)

def create_literal(value):
    return ASTNode('Literal', value=value)

def create_binary_expression(left, operator, right):
    return ASTNode('BinaryExpression', left=left, operator=operator, right=right)

def create_expression_statement(expression):
    return ASTNode('ExpressionStatement', expression=expression)

def create_if_statement(condition, then_body, else_body=None):
    return ASTNode('IfStatement', condition=condition, then=then_body, else=else_body)

def create_function_declaration(name, params, body):
    return ASTNode('FunctionDeclaration', name=name, params=params, body=body)

def create_call_expression(callee, arguments):
    return ASTNode('CallExpression', callee=callee, arguments=arguments)

def create_return_statement(value):
    return ASTNode('ReturnStatement', value=value)

def create_while_loop(condition, body):
    return ASTNode('WhileLoop', condition=condition, body=body)

def create_for_loop(init, condition, update, body):
    return ASTNode('ForLoop', init=init, condition=condition, update=update, body=body)

