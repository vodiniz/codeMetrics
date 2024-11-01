def main():

    nomeCand1= input("Forneça o nome do candidato 1: ")
    numCand1=int(input("Forneça o número do candidato 1: "))
    nomeCand2= input("Forneça o nome do candidato 2: ")
    numCand2= int(input("Forneça o número do candidato 2: "))
    qtdEleitores=int(input("Forneça a quantidade de eleitores: "))
    while qtdEleitores < 3:
        print("A quantidade de eleitores é inferior a 3")
        qtdEleitores=int(input("Forneça a quantidade de eleitores: "))

    print("\n## Votação Iniciada")
    cand1 = 0
    cand2 = 0
    votosValidos = 0
    votosInvalidos = 0
    for i in range(qtdEleitores):
        voto = int(input("Forneça o número do candidato que deseja votar: "))
        if voto == numCand1:
            cand1 = cand1 + 1
            votosValidos = votosValidos + 1
        elif voto == numCand2:
            cand2 = cand2 + 1
            votosValidos = votosValidos + 1
        else:
            votosInvalidos = votosInvalidos + 1
    print("## Votação Encerrada\n")

    print(f"Votos válidos: {(votosValidos/qtdEleitores)*100:.2f}% ({votosValidos} votos)")
    print(f"Votos inválidos: {(votosInvalidos/qtdEleitores)*100:.2f}% ({votosInvalidos} votos)")
    if votosValidos > 0:
        print(f"Votos para {nomeCand1}: {(cand1/votosValidos)*100:.2f}% ({cand1} votos)")
        print(f"Votos para {nomeCand2}: {(cand2/votosValidos)*100:.2f}% ({cand2} votos)")
    else:
        print(f"Votos para {nomeCand1}: 0.00% (0 votos)")
        print(f"Votos para {nomeCand2}: 0.00% (0 votos)")

if __name__ == '__main__':
    main()

