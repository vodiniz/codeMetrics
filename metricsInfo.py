class MetricsInfo:
    def __init__(self, path, filename, name, code_source, description, solution, solution_number, cyclomatic_complexity, radon_cc, unique_operators, 
                 total_statements, avg_nested_depth, total_operators, sloc, cognitive_complexity, complexipy_cognitive_complexity):
        self.path = path
        self.filename = filename
        self.name = name
        self.code_source = code_source
        self.description = description
        self.solution = solution
        self.solution_number = solution_number
        self.cyclomatic_complexity = cyclomatic_complexity
        self.radon_cc = radon_cc
        self.unique_operators = unique_operators
        self.total_statements = total_statements
        self.avg_nested_depth = avg_nested_depth
        self.total_operators = total_operators
        self.sloc = sloc
        self.cognitive_complexity = cognitive_complexity
        self.complexipy_cognitive_complexity = complexipy_cognitive_complexity

    def metrics_to_row_data(self):
        return {
            "name": self.name,
            "code_source": self.code_source,
            "description": self.description,
            "solution": self.solution,
            "solution_number": self.solution_number,
            "cyclomatic_complexity": self.cyclomatic_complexity,
            "unique_operators": self.unique_operators,
            "total_statements": self.total_statements,
            "avg_nested_depth": self.avg_nested_depth,
            "total_operators": self.total_operators,
            "sloc": self.sloc,
            "cognitive_complexity": self.cognitive_complexity,
            "complexipy_cognitive_complexity": self.complexipy_cognitive_complexity
        }
    def metrics_to_tabulate(self):
        return [self.filename,
                self.filename,
                self.cyclomatic_complexity,
                self.radon_cc,
                self.unique_operators,
                self.total_statements,
                self.avg_nested_depth,
                self.total_operators,
                self.sloc,
                self.cognitive_complexity,
                self.complexipy_cognitive_complexity
                ]
    

    def __str__(self):
        return (
            f"MetricsInfo:\n"
            f"  Path: {self.path}\n"
            f"  Filename: {self.filename}\n"
            f"  Name: {self.name}\n"
            f"  Code Source: {self.code_source[:100]}...\n"  # Limita a exibição do código para não sobrecarregar
            f"  Description: {self.description}\n"
            f"  Solution: {self.solution}\n"
            f"  Solution Number: {self.solution_number}\n"
            f"  Cyclomatic Complexity: {self.cyclomatic_complexity}\n"
            f"  Radon CC: {self.radon_cc}\n"
            f"  Unique Operators: {self.unique_operators}\n"
            f"  Total Statements: {self.total_statements}\n"
            f"  Avg Nested Depth: {self.avg_nested_depth}\n"
            f"  Total Operators: {self.total_operators}\n"
            f"  SLOC: {self.sloc}\n"
            f"  Cognitive Complexity: {self.cognitive_complexity}\n"
            f"  Complexipy Cognitive Complexity: {self.complexipy_cognitive_complexity}\n"
        )