def main():
    nome = input('Informe o nome do juiz: ')
    partidas = int(input('Informe a quantidade de partidas: '))
    mImped = 0
    mFalta = 0
    mCartao = 0
    mTempo = 0
    for p in range(partidas):
        print(f'\nPartida {p+1}:')
        imped    =   int(input('. Informe impedimentos.......: '))
        falta    =   int(input('. Informe faltas.............: '))
        cartao   =   int(input('. Informe cartões............: '))
        tempo    = float(input('. Informe tempo de acréscimo.: '))
        mImped = mImped + imped
        mFalta = mFalta + falta
        mCartao = mCartao + cartao
        mTempo = mTempo + tempo
    print(f'\nEstatísticas do juiz {nome}:')
    print(f'. Impedimentos.......: {mImped / partidas:.2f}.')
    print(f'. Faltas.............: {mFalta / partidas:.2f}.')
    print(f'. Cartões............: {mCartao / partidas:.2f}.')
    print(f'. Tempo de acréscimo.: {mTempo / partidas:.2f}.')

if __name__ == '__main__':
    main()