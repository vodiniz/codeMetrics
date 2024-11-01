import ast
import astpretty

from radon.complexity import cc_visit
from radon.raw import analyze

def radon_cc(source_code):
    try:
        # Análise do código fonte para calcular a complexidade ciclomática
        complexity_results = cc_visit(source_code)
        
        # Retorna a complexidade ciclomática total
        total_complexity = sum(result.complexity for result in complexity_results)
        
    except Exception as e:
        total_complexity = -1
        
    return total_complexity


class myComplexity():
    def __init__(self) -> None:
        self.if_complexity = 1
        self.elif_complexity = 1
        self.else_complexity = 0

        self.for_complexity = 1
        self.while_complexity = 1

        self.nested_loop = 0

        self.boolean_operator_complexity = 1

        self.function_complexity = 1

        self.debug = False

        self.complexity = 0

    def get_weight(self, node):

        #     # Verifica se o nó já foi visitado para evitar contar várias vezes
        # if getattr(node, 'visited', False):
        #     return 0

        # # Marca o nó como visitado
        # node.visited = True

        if isinstance(node, ast.If):
    
            # Se não for elif nem else, então é um If
            self.debug_print(f"Linha: {node.lineno}. Nó atual é um If, com complexidade de {self.if_complexity}.")
            return self.if_complexity
            
        elif isinstance(node, ast.For):
            if self.is_inside_loop(node):
                self.debug_print(f"Linha: {node.lineno}. Nó atual é um For aninhado, com complexidade de {self.nested_loop + self.for_complexity}.")
                return self.nested_loop + self.for_complexity
            else:
                self.debug_print(f"Linha: {node.lineno}. Nó atual é um For, com complexidade de {self.for_complexity}.")
                return self.for_complexity
        
        elif isinstance(node, ast.While):
            if self.is_inside_loop(node):
                self.debug_print(f"Linha: {node.lineno}. Nó atual é um While aninhado, com complexidade de {self.while_complexity + self.nested_loop}.")
                return self.while_complexity + self.nested_loop

            self.debug_print(f"Linha: {node.lineno}. Nó atual é um While, com complexidade de {self.while_complexity}.")
            return self.while_complexity
        
        elif isinstance(node, ast.FunctionDef):
            if node.name == "main":
                return 0
            self.debug_print(f"Linha: {node.lineno}. Nó atual é uma função, com complexidade de {self.function_complexity}.")
            return self.function_complexity
        
        return 0

    def is_inside_loop(self, node):
        """
        Função auxiliar que verifica se um nó está dentro de um laço (For ou While).
        """
        # Subir pela árvore de pais para verificar se há um loop acima
        parent = getattr(node, 'parent', None)
        while parent:
            if isinstance(parent, (ast.For, ast.While)):
                return True
            parent = getattr(parent, 'parent', None)
        return False    

    def calculateComplexity(self, source_code: str):
        # print("--------------------COMPLEXIDADE MINHA--------------------------\n")
        self.complexity = 0
        tree = ast.parse(source_code)
        # astpretty.pprint(tree.body[0])

        # Adiciona referência ao pai para cada nó
        for node in ast.walk(tree):
            
            # if hasattr(node, 'lineno') and self.debug:
                # print(f"Nó {type(node).__name__} na linha: {node.lineno}")

            # Define o pai do nó atual

            for child in ast.iter_child_nodes(node):
                child.parent = node
            self.complexity += self.get_weight(node)
        
        # print("--------------------COMPLEXIDADE MINHA--------------------------\n")
        
        return self.complexity

    def debug_print(self, string):
        if self.debug:
            print(string)

def analisar_arquivo(caminho_arquivo):
    with open(caminho_arquivo, 'r') as file:
        codigo = file.read()
    
    # Cria uma instância da classe e calcula a complexidade
    complexity_analyzer = myComplexity()
    complexity_analyzer.debug = False  # Ativa o modo de depuração
    complexity_analyzer.calculateComplexity(codigo)

    # print(f"Complexidade total: {complexity_analyzer.complexity}")

if __name__ == "__main__":
    analisar_arquivo('code/example1_main.py')
