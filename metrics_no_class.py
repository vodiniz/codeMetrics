import ast
import argparse
from cognitive_complexity.api import get_cognitive_complexity
import myComplexity as mc

from metricsInfo import MetricsInfo

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
    # tree = ast.parse(source_code)
    # complexity_counter = CyclomaticComplexityCounter()
    # complexity_counter.visit(tree)
    # return complexity_counter.complexity

    complexity_analyzer = mc.myComplexity()
    complexity_analyzer.debug = True  # Ativa o modo de depuração
    return complexity_analyzer.calculateComplexity(source_code)

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



def calculate_cognitive_complexity(source_code):
    """
    Calculates the cognitive complexity of the source code.

    :param source_code: The source code to be evaluated as a string.
    :return: The cognitive complexity number.
    """
    tree = ast.parse(source_code).body[0]
    
    
    try:
        cognitive = get_cognitive_complexity(tree)
    except:
        cognitive = 1
    return cognitive


from radon.complexity import cc_visit
from radon.raw import analyze

def radon_cc(source_code):
    try:
        # Análise do código fonte para calcular a complexidade ciclomática
        complexity_results = cc_visit(source_code)
        
        # Retorna a complexidade ciclomática total
        total_complexity = sum(result.complexity for result in complexity_results)
        
        print("------------------RADON---------------------\n")
        for result in complexity_results:
            print(result)
    except Exception as e:
        total_complexity = -1
    print("------------------RADON---------------------\n")
    
    return total_complexity


import subprocess

def run_complexipy_command(file_path):
    # Caminho para o diretório do projeto e do ambiente virtual
    project_dir = '/home/vodiniz/Prog/codeMetrics'
    virtualenv_activate_script = os.path.join(project_dir, '.env/bin/activate')
    
    # Comando para ativar o ambiente virtual e executar o complexipy
    command = f"source {virtualenv_activate_script} && complexipy {file_path} -l file -o"
    
    try:
        # Executa o comando no diretório do projeto
        result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=project_dir, check=True)
        
        # Caminho do arquivo CSV gerado
        csv_file_path = os.path.join(project_dir, 'complexipy.csv')
        
        return csv_file_path
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        print(f"Saída do erro: {e.stderr}")
        return None
    

    

import pandas as pd
def read_complexipy_csv(csv_file_path):
    try:
        # Lê o arquivo CSV usando pandas
        df = pd.read_csv(csv_file_path)
        
        # Verifica se as colunas esperadas estão presentes
        if 'Path' not in df.columns or 'Cognitive Complexity' not in df.columns:
            raise ValueError("O arquivo CSV não contém as colunas esperadas.")
        
        # Cria um dicionário com Path como chave e Cognitive Complexity como valor
        complexity_dict = dict(zip(df['Path'], df['Cognitive Complexity']))
        
        return complexity_dict
    
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return None

from tabulate import tabulate
from simple_colors import *
import os

def print_code_metrics(data, show_headers=False):
    headers = [
        "Path", "File", "Cyclomatic Complexity", "Radon CC",
        "Unique Operators", "Total Statements", 
        "Avg Nested Depth", "Total Operators", "SLOC", "Cognitive Complexity", "Complexipy Cog. C."
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

def process_file(filename, source_code, complexity_dict):
    """Processa um único arquivo e retorna suas métricas."""
    try:

        
        cognitive_complexity = complexity_dict.get(filename, 'N/A')
        with open(filename, 'r') as file:
            print(f"---------------{filename}-------------------")

            code = source_code if source_code else file.read()

            return MetricsInfo(
                path=filename,
                filename=filename,
                cyclomatic_complexity=calculate_cyclomatic_complexity(code),
                radon_cc=radon_cc(code),
                unique_operators=calculate_unique_operators(code),
                total_statements=calculate_total_statements(code),
                avg_nested_depth=calculate_average_depth(code),
                total_operators=calculate_total_operators(code),
                sloc=calculate_sloc(code),
                cognitive_complexity=calculate_cognitive_complexity(code),
                complexipy_cognitive_complexity=cognitive_complexity
            )
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
        metrics = process_file(path, None, complexity_dict)
        run_complexipy_command(path)
        if metrics:
            data.append(metrics)
    elif os.path.isdir(path):
        run_complexipy_command(path)
        # Process all files in the directory
    # Get the path from arguments
    path = args.path

    data = []
    show_headers = True

    csv_file_path = run_complexipy_command(path)
    complexity_dict = read_complexipy_csv(csv_file_path)

    if os.path.isfile(path):
        # Process a single file
        metrics = process_file(path, None, complexity_dict)
        run_complexipy_command(path)
        if metrics:
            data.append(metrics)
    elif os.path.isdir(path):
        run_complexipy_command(path)
        # Process all files in the directory
        for root, dirs, files in os.walk(path):
            for file in files:
                # Assuming you want to process only Python files
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    metrics = process_file(file_path, None, complexity_dict)
                    if metrics:
                        data.append(metrics)
        show_headers = True
    else:
        print(f"Error: The path '{path}' is neither a file nor a directory.")
        return

    # sort metrics
    data = sorted(data, key=lambda x: x[1])

    # Print all data with headers
    print_code_metrics(data, show_headers)




# Ensure that this script is run directly
if __name__ == "__main__":
    main()