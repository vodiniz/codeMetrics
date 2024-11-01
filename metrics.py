import ast
import argparse
import os
import subprocess
import pandas as pd
from cognitive_complexity.api import get_cognitive_complexity
from radon.complexity import cc_visit
from radon.raw import analyze
from tabulate import tabulate
from simple_colors import *
import myComplexity as mc

from metricsInfo import MetricsInfo

class Metrics:
    def __init__(self):
        self.complexity_dict = {}

    def calculate_unique_operators(self, source_code):
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

    def calculate_total_statements(self, source_code):
        tree = ast.parse(source_code)
        return sum(isinstance(node, ast.stmt) for node in ast.walk(tree))

    def calculate_cyclomatic_complexity(self, source_code):
        complexity_analyzer = mc.myComplexity()
        return complexity_analyzer.calculateComplexity(source_code)

    def calculate_average_depth(self, source_code):
        tree = ast.parse(source_code)
        depth_counter = self.NestedBlockDepthCounter()
        depth_counter.visit(tree)
        return depth_counter.get_average_depth()

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
            return self.total_depth / self.block_count if self.block_count else 0

    def calculate_total_operators(self, source_code):
        tree = ast.parse(source_code)
        operator_counter = self.OperatorCounter()
        operator_counter.visit(tree)
        return operator_counter.operator_count

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

    def calculate_sloc(self, source_code):
        lines = source_code.splitlines()
        return sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))

    def calculate_cognitive_complexity(self, source_code):
        tree = ast.parse(source_code).body[0]
        try:
            cognitive = get_cognitive_complexity(tree)
        except:
            cognitive = 1
        return cognitive

    def radon_cc(self, source_code):
        try:
            complexity_results = cc_visit(source_code)
            return sum(result.complexity for result in complexity_results)
        except Exception as e:
            return -1

    def run_complexipy_command(self, file_path):
        project_dir = '/home/vodiniz/Prog/codeMetrics'
        virtualenv_activate_script = os.path.join(project_dir, '.env/bin/activate')
        command = f"source {virtualenv_activate_script} && complexipy {file_path} -l file -o"
        try:
            result = subprocess.run(command, shell=True, text=True, capture_output=True, cwd=project_dir, check=True)
            csv_file_path = os.path.join(project_dir, 'complexipy.csv')
            return csv_file_path
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o comando: {e}")
            print(f"Saída do erro: {e.stderr}")
            return None

    def read_complexipy_csv(self, csv_file_path):
        try:
            df = pd.read_csv(csv_file_path)
            if 'Path' not in df.columns or 'Cognitive Complexity' not in df.columns:
                raise ValueError("O arquivo CSV não contém as colunas esperadas.")
            self.complexity_dict = dict(zip(df['Path'], df['Cognitive Complexity']))
        except Exception as e:
            print(f"Erro ao ler o arquivo CSV: {e}")
    def print_code_metrics(self, data, show_headers=False):
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

    def process_file(self, filename, source_code):
            try:
                cognitive_complexity = self.complexity_dict.get(filename, 'N/A')
                with open(filename, 'r') as file:
                    code = source_code if source_code else file.read()
                    return MetricsInfo(
                        path=filename,
                        filename=filename,
                        name=filename,
                        code_source=code,
                        description="",
                        solution="",
                        solution_number="",
                        cyclomatic_complexity=self.calculate_cyclomatic_complexity(code),
                        radon_cc=self.radon_cc(code),
                        unique_operators=self.calculate_unique_operators(code),
                        total_statements=self.calculate_total_statements(code),
                        avg_nested_depth=self.calculate_average_depth(code),
                        total_operators=self.calculate_total_operators(code),
                        sloc=self.calculate_sloc(code),
                        cognitive_complexity=self.calculate_cognitive_complexity(code),
                        complexipy_cognitive_complexity=cognitive_complexity
                    )
            except FileNotFoundError:
                print(f"Error: The file '{filename}' was not found.")
            except Exception as e:
                print(f"Error opening the file: {e}")
    @staticmethod
    def main():
        parser = argparse.ArgumentParser(description="Process files or directories for code metrics.")
        parser.add_argument('path', type=str, help="The file or directory to process.")
        args = parser.parse_args()
        path = args.path
        data = []
        tabulate_data = []

        # Instanciando Metrics para acessar métodos que não podem ser estáticos
        metrics_instance = Metrics()

        csv_file_path = metrics_instance.run_complexipy_command(path)
        if csv_file_path:
            metrics_instance.read_complexipy_csv(csv_file_path)

        if os.path.isfile(path):
            metrics = metrics_instance.process_file(path, None)
            if metrics:
                data.append(metrics)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        metrics = metrics_instance.process_file(file_path, None)
                        if metrics:
                            data.append(metrics)
                            tabulate_data.append(metrics.metrics_to_tabulate())
        else:
            print(f"Error: The path '{path}' is neither a file nor a directory.")
            return

        tabulate_data.sort(key=lambda x: x[1])
        metrics_instance.print_code_metrics(tabulate_data, show_headers=True)


# Ensure that this script is run directly
if __name__ == "__main__":

    Metrics.main()