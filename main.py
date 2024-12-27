# main.py
import sys
import os
from main_language import Lexer, Parser, Interpreter, report_error, pretty_print

def run_code(code: str, filename="<stdin>"):
    """
    Tokenize, parse, and interpret the provided code.
    """
    try:
        # Step 1: Tokenize the code using the Lexer
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print("Tokens:")  # Show the tokens (debugging feature)
        pretty_print(tokens)
        
        # Step 2: Parse the tokens using the Parser
        parser = Parser(lexer)
        ast = parser.parse()
        print("AST:")  # Show the AST (debugging feature)
        pretty_print(ast)
        
        # Step 3: Interpret the AST using the Interpreter
        interpreter = Interpreter()
        result = interpreter.interpret(ast)
        print("Execution Result:")
        print(result)
    
    except Exception as e:
        # Enhanced error reporting
        report_error(f"Error in {filename}: {str(e)}")

def run_repl():
    """
    Run the REPL (Read-Eval-Print Loop) for interactive code execution.
    """
    print("Welcome to the Main Language REPL! Type 'exit' to quit.")
    
    context = {}
    
    while True:
        try:
            # Read input from user
            code = input("> ")
            
            if code.strip().lower() == "exit":
                print("Exiting REPL.")
                break
            
            # Execute code
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(lexer)
            ast = parser.parse()
            
            # In the REPL, we'll keep track of variable states in a context (dictionary)
            interpreter = Interpreter(context)
            result = interpreter.interpret(ast)
            
            print(f"Result: {result}")
        
        except KeyboardInterrupt:
            print("\nExiting REPL.")
            break
        except Exception as e:
            report_error(f"Runtime error: {e}")

def run_file(filename: str):
    """
    Run the code from a file.
    """
    try:
        with open(filename, 'r') as file:
            code = file.read()
        run_code(code, filename)
    except FileNotFoundError:
        report_error(f"File '{filename}' not found.")
    except Exception as e:
        report_error(f"Error reading {filename}: {str(e)}")

def main():
    """
    Main function to handle user input or file execution.
    """
    if len(sys.argv) > 1:
        # If a file is passed as an argument, run the code from the file
        file_path = sys.argv[1]
        run_file(file_path)
    else:
        # If no arguments, enter REPL mode
        run_repl()

if __name__ == "__main__":
    main()
