# utils.py

def report_error(message, line=None, column=None):
    """
    Utility function for reporting errors in the code.
    Prints a formatted error message with optional line and column information.
    """
    error_message = f"Error: {message}"
    if line is not None and column is not None:
        error_message += f" at line {line}, column {column}"
    print(error_message)
    # You can raise an exception if you want to terminate the process
    # raise SyntaxError(error_message)

def is_number(value):
    """
    Check if the value is a number (either integer or float).
    """
    try:
        float(value)  # Try to cast to float
        return True
    except ValueError:
        return False

def is_string(value):
    """
    Check if the value is a string.
    """
    return isinstance(value, str)

def is_boolean(value):
    """
    Check if the value is a boolean.
    """
    return isinstance(value, bool)

def pretty_print(ast, indent=0):
    """
    Pretty prints the AST for debugging purposes.
    """
    indent_str = " " * indent
    if isinstance(ast, list):
        for node in ast:
            pretty_print(node, indent)
    else:
        print(f"{indent_str}{ast.type}")
        for key, value in ast.__dict__.items():
            if isinstance(value, ASTNode):
                print(f"{indent_str}  {key}:")
                pretty_print(value, indent + 4)
            elif isinstance(value, list):
                print(f"{indent_str}  {key}:")
                pretty_print(value, indent + 4)
            else:
                print(f"{indent_str}  {key}: {value}")
