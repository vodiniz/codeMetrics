import os
from metrics import Metrics
from datasets import load_dataset
from metricsInfo import MetricsInfo

import csv

class ProcessDataset:
    def __init__(self) -> None:
        self.csv_path = 'metrics_dataset.csv'
        self.csv_columns = [
        "name", "description", "solution", "solution_number",
        "cyclomatic_complexity", "unique_operators", "total_statements",
        "avg_nested_depth", "total_operators", "sloc", "cognitive_complexity"
        ]
        file_exists = os.path.isfile(self.csv_path)

        with open(self.csv_path, mode='a', newline='') as file:
            self.csv_writer = csv.DictWriter(file, fieldnames=self.csv_columns)
            if not self.csv_writer:
                self.csv_writer.writeheader()
        

    def write_row(self, row_data):
        self.csv_writer.writerow(row_data)
        

    def run(self):

        # Carrega o dataset deepmind/code_contests do Hugging Face
        dataset = load_dataset('deepmind/code_contests')

        # Acessa o conjunto de dados de treinamento
        train_dataset = dataset['train']

        total_lines = len(train_dataset)

        print(total_lines)

        # Contador para nomear os arquivos


        for idx,line in enumerate(train_dataset):
            name = line['name']
            description = line['description']
            solutions = line['solutions']  # Acessa a coluna 'solutions' de cada exemplo
            languages = solutions['language']  # Extrai o vetor 'language'
            cont = 0
            solution_counter = 0

            for language in languages:
                if language == 3:

                    solution = solutions['solution'][cont]

                    file_name = f"temp.py"

                    # Salva a solução em um arquivo .py
                    with open(file_name, 'w') as file:
                        file.write(solution)
                    metrics = Metrics()
                    metrics_info: MetricsInfo = metrics.process_file("temp.py", solution)

                    metrics_info.name = name if name is not None else 'None'
                    metrics_info.description = description if description is not None else 'None'
                    metrics_info.solution = solution
                    metrics_info.solution_number = solution_counter
                    # Incrementa o contador
                    solution_counter += 1

                    print(metrics_info)

                    
                    break

                cont += 1
            percent_done = (idx + 1) / total_lines * 100

            # if solution_counter >= 100:
            #     break;

        
        print(f"Progresso: {percent_done:.2f}%")



if __name__ == "__main__":
    process_dataset = ProcessDataset()
    process_dataset.run()