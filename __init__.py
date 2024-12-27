# main_language/__init__.py

# Import key components to make them accessible when importing the main_language module
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .ast import ASTNode
from .utils import report_error, is_number, pretty_print

# Optionally, expose specific utility functions or classes here for ease of use
 
