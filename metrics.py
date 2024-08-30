import ast
import argparse

def calculate_unique_operators(source_code):
    """
    Calculate the total number of unique operators found in the source code.

    :param source_code: The source code to be evaluated as a string.
    :return: The total number of unique operators.
    """
    # Parse the source code into an Abstract Syntax Tree (AST)
    tree = ast.parse(source_code)

    unique_operators = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp):
            unique_operators.add(type(node.op))
        elif isinstance(node, ast.UnaryOp):
            unique_operators.add(type(node.op))
        elif isinstance(node, ast.BoolOp):
            unique_operators.add(type(node.op))
        elif isinstance(node, ast.Compare):
            for op in node.ops:
                unique_operators.add(type(op))

    return len(unique_operators)

def calculate_total_statements(source_code):
    """
    Counts the total number of statements in the source code.

    :param source_code: The source code to be evaluated as a string.
    :return: The total number of statements.
    """
    tree = ast.parse(source_code)
    statement_count = sum(isinstance(node, ast.stmt) for node in ast.walk(tree))
    return statement_count

class CyclomaticComplexityCounter(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 1  # Initial count for linear flow

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_And(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Or(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.complexity += 1
        self.generic_visit(node)

def calculate_cyclomatic_complexity(source_code):
    """
    Calculates the cyclomatic complexity using AST.

    :param source_code: The source code to be evaluated as a string.
    :return: The cyclomatic complexity number.
    """
    tree = ast.parse(source_code)
    complexity_counter = CyclomaticComplexityCounter()
    complexity_counter.visit(tree)
    return complexity_counter.complexity

class NestedBlockDepthCounter(ast.NodeVisitor):
    def __init__(self):
        self.total_depth = 0
        self.block_count = 0
        self.current_depth = 0

    def visit(self, node):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
            self.current_depth += 1
            self.total_depth += self.current_depth
            self.block_count += 1
            self.generic_visit(node)
            self.current_depth -= 1
        else:
            self.generic_visit(node)

    def get_average_depth(self):
        if self.block_count == 0:
            return 0
        return self.total_depth / self.block_count

def calculate_average_depth(source_code):
    """
    Calculates the average depth of nested blocks in the source code.

    :param source_code: The source code to be evaluated as a string.
    :return: The average depth of nested blocks.
    """
    tree = ast.parse(source_code)
    depth_counter = NestedBlockDepthCounter()
    depth_counter.visit(tree)
    return depth_counter.get_average_depth()

class OperatorCounter(ast.NodeVisitor):
    def __init__(self):
        self.operator_count = 0

    def visit_BinOp(self, node):
        self.operator_count += 1
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        self.operator_count += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.operator_count += 1
        self.generic_visit(node)

    def visit_Compare(self, node):
        self.operator_count += len(node.ops)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        self.operator_count += 1
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.operator_count += 1
        self.generic_visit(node)

def calculate_total_operators(source_code):
    """
    Calculates the total number of operators in the source code.

    :param source_code: The source code to be evaluated as a string.
    :return: The total number of operators.
    """
    tree = ast.parse(source_code)
    operator_counter = OperatorCounter()
    operator_counter.visit(tree)
    return operator_counter.operator_count

def calculate_sloc(source_code):
    """
    Calculates the Source Lines of Code (SLOC) from the source code.

    :param source_code: The source code to be evaluated as a string.
    :return: The number of SLOC.
    """
    lines = source_code.splitlines()
    sloc = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
    return sloc

class CognitiveComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexity = 0
        self.nesting_level = 0
        self.max_nesting = 0
    
    def visit_FunctionDef(self, node):
        self.nesting_level = 0
        self.generic_visit(node)
        self.complexity += self.max_nesting
    
    def visit_If(self, node):
        self._handle_control_flow()
        self.generic_visit(node)
    
    def visit_For(self, node):
        self._handle_control_flow()
        self.generic_visit(node)
    
    def visit_While(self, node):
        self._handle_control_flow()
        self.generic_visit(node)
    
    def visit_Try(self, node):
        self._handle_control_flow()
        self.generic_visit(node)
    
    def visit_ExceptHandler(self, node):
        self._handle_control_flow()
        self.generic_visit(node)
    
    def _handle_control_flow(self):
        self.nesting_level += 1
        self.max_nesting = max(self.max_nesting, self.nesting_level)
    
    def generic_visit(self, node):
        self.nesting_level -= 1
        super().generic_visit(node)

def calculate_cognitive_complexity(source_code):
    """
    Calculates the cognitive complexity of the source code.

    :param source_code: The source code to be evaluated as a string.
    :return: The cognitive complexity number.
    """
    tree = ast.parse(source_code)
    visitor = CognitiveComplexityVisitor()
    visitor.visit(tree)
    return visitor.complexity


from tabulate import tabulate
from simple_colors import *
import os

def print_code_metrics(data, show_headers=False):
    headers = [
        "Path", "File", "Cyclomatic Complexity", 
        "Unique Operators", "Total Statements", 
        "Avg Nested Depth", "Total Operators", "SLOC", "Cognitive Complexity"
    ]
    
    if show_headers:
        # Formatando a tabela com cabeçalhos
        table = tabulate(data, headers, tablefmt="fancy_grid", numalign="left", stralign="left")
    else:
        # Formatando a tabela sem cabeçalhos
        table = tabulate(data, headers=[], tablefmt="fancy_grid", numalign="left", stralign="left")

    # Colorindo apenas os cabeçalhos
    if show_headers:
        colored_headers = [f"\x1b[1;35m{header}\x1b[0m" for header in headers]
        for i, header in enumerate(headers):
            table = table.replace(header, colored_headers[i])

    print(table)

def process_file(filename):
    """Processa um único arquivo e retorna suas métricas."""
    try:
        with open(filename, 'r') as file:
            source_code = file.read()
            metrics = [
                filename,
                filename,
                calculate_cyclomatic_complexity(source_code),
                calculate_unique_operators(source_code),
                calculate_total_statements(source_code),
                calculate_average_depth(source_code),
                calculate_total_operators(source_code),
                calculate_sloc(source_code),
                calculate_cognitive_complexity(source_code)
            ]
            return metrics
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except Exception as e:
        print(f"Error opening the file: {e}")
        return None

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process files or directories passed as command-line arguments.")
    
    # Add the argument for the filename or directory
    parser.add_argument('path', type=str, help="The name of the file or directory to be processed.")
    
    # Parse command-line arguments
    args = parser.parse_args()
    
    # Get the path from arguments
    path = args.path

    data = []
    show_headers = True

    if os.path.isfile(path):
        # Process a single file
        metrics = process_file(path)
        if metrics:
            data.append(metrics)
    elif os.path.isdir(path):
        # Process all files in the directory
        for root, dirs, files in os.walk(path):
            for file in files:
                # Assuming you want to process only Python files
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    metrics = process_file(file_path)
                    if metrics:
                        data.append(metrics)
        show_headers = True
    else:
        print(f"Error: The path '{path}' is neither a file nor a directory.")
        return

    # Print all data with headers
    print_code_metrics(data, show_headers)

# Ensure that this script is run directly
if __name__ == "__main__":
    main()