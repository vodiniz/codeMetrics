import math

# Função calculaComprimento
def calculaComprimento(reta):
    comprimento = math.sqrt((reta["B"]["X"] - reta["A"]["X"]) ** 2 + (reta["B"]["Y"] - reta["A"]["Y"]) ** 2)
    return comprimento

# programa principal
x = float(input('Informe a coordenada X de A: '))
y = float(input('Informe a coordenada Y de A: '))
A = { "X": x, "Y": y }
x = float(input('Informe a coordenada X de B: '))
y = float(input('Informe a coordenada Y de B: '))
B = { "X": x, "Y": y }
reta = { "A": A, "B": B}
print(f'\nDistância entre os pontos A e B: {calculaComprimento(reta):.2f}')