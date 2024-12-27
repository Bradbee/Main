class ASTNode:
    """
    Base class for all AST nodes.
    """
    def __init__(self, node_type, children=None):
        self.type = node_type
        self.children = children or []

class ProgramNode(ASTNode):
    """
    Represents the entire program (root node).
    """
    def __init__(self, children=None):
        super().__init__("Program", children)

class VariableDeclarationNode(ASTNode):
    """
    Represents a variable declaration (e.g., let x = 10).
    """
    def __init__(self, name, initializer):
        super().__init__("VariableDeclaration")
        self.value = {"name": name, "initializer": initializer}

class FunctionDeclarationNode(ASTNode):
    """
    Represents a function declaration (e.g., function foo() {}).
    """
    def __init__(self, name, parameters, body, async_flag=False):
        super().__init__("FunctionDeclaration")
        self.value = {
            "name": name,
            "parameters": parameters,
            "body": body,
            "async": async_flag
        }

class ClassDeclarationNode(ASTNode):
    """
    Represents a class declaration (e.g., class MyClass {}).
    """
    def __init__(self, name, super_class, body):
        super().__init__("ClassDeclaration")
        self.value = {"name": name, "superClass": super_class, "body": body}

class ControlFlowNode(ASTNode):
    """
    Represents control flow statements (e.g., if, while).
    """
    def __init__(self, keyword, condition, body):
        super().__init__("ControlFlow")
        self.value = {"keyword": keyword, "condition": condition, "body": body}

class ConcurrencyNode(ASTNode):
    """
    Represents concurrency constructs (e.g., spawn, join).
    """
    def __init__(self, keyword, target):
        super().__init__("Concurrency")
        self.value = {"keyword": keyword, "target": target}

class MemoryManagementNode(ASTNode):
    """
    Represents memory management constructs (e.g., alloc, free, gc).
    """
    def __init__(self, keyword, variable=None):
        super().__init__("MemoryManagement")
        self.value = {"keyword": keyword, "variable": variable}

class CryptographyNode(ASTNode):
    """
    Represents cryptography functions (e.g., encrypt, decrypt, hash).
    """
    def __init__(self, keyword, argument):
        super().__init__("Cryptography")
        self.value = {"keyword": keyword, "argument": argument}

class ReflectionNode(ASTNode):
    """
    Represents reflection functions (e.g., reflect, proxy).
    """
    def __init__(self, keyword, argument):
        super().__init__("Reflection")
        self.value = {"keyword": keyword, "argument": argument}

class TryCatchNode(ASTNode):
    """
    Represents a try-catch-finally block.
    """
    def __init__(self, try_block, catch_block=None, finally_block=None):
        super().__init__("TryCatch")
        self.value = {
            "try": try_block,
            "catch": catch_block,
            "finally": finally_block
        }
