import math
import re
import random
import string

class Utils:
    """
    A utility class containing various helper functions used across the language.
    """

    @staticmethod
    def is_number(value):
        """
        Check if a value is a valid number (int or float).
        """
        try:
            float(value)  # Try casting the value to a float
            return True
        except ValueError:
            return False

    @staticmethod
    def is_integer(value):
        """
        Check if a value is a valid integer.
        """
        try:
            int(value)  # Try casting the value to an integer
            return True
        except ValueError:
            return False

    @staticmethod
    def is_string(value):
        """
        Check if a value is a valid string.
        """
        return isinstance(value, str)

    @staticmethod
    def is_boolean(value):
        """
        Check if a value is a boolean (True or False).
        """
        return isinstance(value, bool)

    @staticmethod
    def is_callable(value):
        """
        Check if a value is callable (a function or method).
        """
        return callable(value)

    @staticmethod
    def to_string(value):
        """
        Convert any value to a string.
        """
        return str(value)

    @staticmethod
    def to_boolean(value):
        """
        Convert a value to a boolean (True or False).
        """
        if value in {0, '0', 'false', 'False', 'no', 'No', 'n'}:
            return False
        return bool(value)

    @staticmethod
    def to_number(value):
        """
        Convert a value to a number (int or float).
        """
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Cannot convert {value} to number.")

    @staticmethod
    def to_integer(value):
        """
        Convert a value to an integer.
        """
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Cannot convert {value} to integer.")

    @staticmethod
    def generate_random_string(length=10):
        """
        Generate a random string of a given length consisting of alphanumeric characters.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def generate_random_number(min_value=0, max_value=100):
        """
        Generate a random number between a specified range.
        """
        return random.randint(min_value, max_value)

    @staticmethod
    def validate_identifier(identifier):
        """
        Validate an identifier (variable or function name).
        """
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', identifier):
            raise ValueError(f"Invalid identifier: {identifier}. Must start with a letter or underscore.")
        return True

    @staticmethod
    def is_truthy(value):
        """
        Check if a value is truthy (non-zero, non-null, etc.).
        """
        return bool(value)

    @staticmethod
    def is_falsy(value):
        """
        Check if a value is falsy (0, empty, null, etc.).
        """
        return not bool(value)

    @staticmethod
    def apply_operator(left, right, operator):
        """
        Apply an operator to two values (e.g., +, -, *, /).
        """
        if operator == "+":
            return left + right
        elif operator == "-":
            return left - right
        elif operator == "*":
            return left * right
        elif operator == "/":
            if right == 0:
                raise ZeroDivisionError("Division by zero.")
            return left / right
        elif operator == "%":
            return left % right
        elif operator == "**":
            return left ** right
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    @staticmethod
    def apply_comparison(left, right, operator):
        """
        Apply a comparison operator to two values (e.g., ==, !=, <, >, <=, >=).
        """
        if operator == "==":
            return left == right
        elif operator == "!=":
            return left != right
        elif operator == "<":
            return left < right
        elif operator == ">":
            return left > right
        elif operator == "<=":
            return left <= right
        elif operator == ">=":
            return left >= right
        else:
            raise ValueError(f"Unsupported comparison operator: {operator}")

    @staticmethod
    def apply_logical(left, right, operator):
        """
        Apply a logical operator to two values (e.g., AND, OR).
        """
        if operator == "&&":
            return left and right
        elif operator == "||":
            return left or right
        else:
            raise ValueError(f"Unsupported logical operator: {operator}")

    @staticmethod
    def get_type(value):
        """
        Return the type of a given value as a string.
        """
        if isinstance(value, bool):
            return "boolean"
        elif isinstance(value, int):
            return "integer"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "string"
        elif value is None:
            return "null"
        elif callable(value):
            return "function"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        else:
            return "unknown"
    
    @staticmethod
    def deep_copy(value):
        """
        Create a deep copy of a value (useful for complex objects or data structures).
        """
        if isinstance(value, dict):
            return {key: Utils.deep_copy(val) for key, val in value.items()}
        elif isinstance(value, list):
            return [Utils.deep_copy(item) for item in value]
        else:
            return value
