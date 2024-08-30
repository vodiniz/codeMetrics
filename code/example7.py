# Entrada
p = float(input("Digite seu peso (em kg): "))
a = float(input("Digite sua altura (em metros): "))
q = float(input("Digite a circunferência do seu quadril (em cm): "))

# Processamento
imc = p / (a ** 2)
iac = (q / a ** 1.5) - 18

# Saída
print(f"IMC = {imc:.3f}")
print(f"IAC = {iac:.3f}")
