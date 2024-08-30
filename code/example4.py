def Situacao(aluno):
    if aluno['nota'] >= 6:
        return 'APROVADO'
    elif aluno['nota'] >= 3:
        return 'EXAME ESPECIAL'
    else:
        return 'REPROVADO'

qtdAlunos = int(input('Digite a quantidade de alunos: '))
alunos = []
for a in range(qtdAlunos):
    nome = input(f'\nDigite o nome do aluno {a+1}: ')
    nota = float(input(f'Digite a nota do aluno {a+1}: '))
    alunos.append({'nome': nome, 'nota': nota})

print('\nSituação dos alunos:')
for a in range(qtdAlunos):
    print(f'{a+1}. {alunos[a]["nome"]} - Nota: {alunos[a]["nota"]:.2f} - {Situacao(alunos[a])}')
