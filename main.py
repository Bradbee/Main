import time
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from ast import *
from utils import Utils

class MainInterpreter:
    def __init__(self):
        self.parser = Parser()
        self.interpreter = Interpreter()
        self.debug_mode = False
        self.execution_log = []

    def toggle_debug_mode(self):
        """
        Toggle debugging mode on and off.
        """
        self.debug_mode = not self.debug_mode
        print(f"Debug mode {'enabled' if self.debug_mode else 'disabled'}.")

    def log_execution(self, message):
        """
        Log detailed execution steps in debug mode.
        """
        if self.debug_mode:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            self.execution_log.append(f"[{timestamp}] {message}")
            print(f"DEBUG: {message}")
    
    def run(self, code):
        """
        Run the code through the lexer, parser, and interpreter.
        """
        try:
            # Step 1: Lexical Analysis (Tokenization)
            self.log_execution("Starting lexical analysis...")
            lexer = Lexer(code)  # Pass the source code to the lexer here
            tokens = lexer.tokenize()
            self.log_execution(f"Tokenization complete. {len(tokens)} tokens generated.")
            
            # Step 2: Parsing (Building AST)
            self.log_execution("Starting parsing...")
            ast = self.parser.parse(tokens)
            self.log_execution("Parsing complete. AST generated.")
            
            # Step 3: Interpretation (Executing AST)
            self.log_execution("Starting interpretation...")
            self.interpreter.interpret(ast)
            self.log_execution("Interpretation complete.")
        
        except Exception as e:
            self.log_execution(f"Error during execution: {str(e)}")
            print(f"Error: {str(e)}")
    
    def handle_user_input(self):
        """
        Prompt the user for code input and run the interpreter.
        """
        print("Welcome to Main Language Interpreter.")
        while True:
            try:
                code = input("Enter code (or 'exit' to quit): ")
                if code.lower() == 'exit':
                    print("Exiting interpreter.")
                    break
                self.run(code)
            except KeyboardInterrupt:
                print("\nExiting interpreter.")
                break

    def handle_file_input(self, filepath):
        """
        Load code from a file and run the interpreter.
        """
        try:
            with open(filepath, 'r') as file:
                code = file.read()
                self.run(code)
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found.")
        except Exception as e:
            print(f"Error: {str(e)}")

    def execute_concurrent_tasks(self, tasks):
        """
        Execute multiple tasks concurrently.
        """
        self.log_execution("Starting concurrent tasks...")
        from threading import Thread
        
        threads = []
        for task in tasks:
            thread = Thread(target=self.run, args=(task,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()  # Wait for all threads to finish
        self.log_execution("Concurrent tasks completed.")

    def memory_management_demo(self):
        """
        Demonstrate memory management features like alloc and free.
        """
        self.log_execution("Starting memory management demo...")
        try:
            memory_block = Utils.generate_random_string(10)
            self.log_execution(f"Allocated memory block: {memory_block}")
            
            # Freeing the memory block (simulated)
            memory_block = None
            self.log_execution("Memory block freed.")
            
            # Simulate garbage collection
            gc_result = self.simulate_garbage_collection()
            self.log_execution(f"Garbage collection result: {gc_result}")
        except Exception as e:
            self.log_execution(f"Memory management error: {str(e)}")

    def simulate_garbage_collection(self):
        """
        Simulate garbage collection by clearing unused objects.
        """
        # This is just a mock. Actual garbage collection would be handled by Python's GC.
        self.log_execution("Simulating garbage collection...")
        return "Collected unused objects."

    def cryptography_demo(self):
        """
        Demonstrate cryptographic operations like hashing and encryption.
        """
        self.log_execution("Starting cryptography demo...")
        try:
            text = "This is a secret message."
            encrypted_text = self.encrypt_text(text)
            self.log_execution(f"Encrypted text: {encrypted_text}")
            
            decrypted_text = self.decrypt_text(encrypted_text)
            self.log_execution(f"Decrypted text: {decrypted_text}")
            
            hashed_text = self.hash_text(text)
            self.log_execution(f"Hashed text: {hashed_text}")
        except Exception as e:
            self.log_execution(f"Cryptography error: {str(e)}")

    def encrypt_text(self, text):
        """
        Mock encryption function (caesar cipher).
        """
        return ''.join(chr((ord(c) + 3) % 256) for c in text)

    def decrypt_text(self, text):
        """
        Mock decryption function (reverse of caesar cipher).
        """
        return ''.join(chr((ord(c) - 3) % 256) for c in text)

    def hash_text(self, text):
        """
        Mock hash function (using Python's hash).
        """
        return hash(text)

    def reflection_demo(self):
        """
        Demonstrate reflection features like proxies and dynamic behavior.
        """
        self.log_execution("Starting reflection demo...")
        try:
            obj = {"name": "Alice", "age": 30}
            proxy = self.create_proxy(obj)
            self.log_execution(f"Proxy object: {proxy}")
        except Exception as e:
            self.log_execution(f"Reflection error: {str(e)}")

    def create_proxy(self, obj):
        """
        Create a proxy for an object that intercepts attribute access.
        """
        class Proxy:
            def __init__(self, obj):
                self.obj = obj

            def __getattr__(self, name):
                if name in self.obj:
                    return self.obj[name]
                else:
                    return f"Attribute '{name}' not found in object."

        return Proxy(obj)


# Main program execution
if __name__ == "__main__":
    interpreter = MainInterpreter()

    # Toggle debug mode if needed
    interpreter.toggle_debug_mode()

    # Run a simple demo
    code_demo = """
    let a = 5;
    let b = 10;
    function add(x, y) { return x + y; }
    let sum = add(a, b);
    print(sum);
    """
    interpreter.run(code_demo)

    # Demonstrate concurrency
    tasks = [
        "let a = 5; print(a);",
        "let b = 10; print(b);"
    ]
    interpreter.execute_concurrent_tasks(tasks)

    # Demonstrate memory management
    interpreter.memory_management_demo()

    # Demonstrate cryptography
    interpreter.cryptography_demo()

    # Demonstrate reflection
    interpreter.reflection_demo()

    # Handle user input for interactive mode
    interpreter.handle_user_input()

