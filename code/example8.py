def realizaCalculos(termos, raio):
    pi_somatorio = 0
    for n in range(termos):
        pi_somatorio = pi_somatorio + (-1) ** n * (4 / (2 * n + 1))
    volume_esfera = 4/3 * pi_somatorio * raio ** 3
    return round(pi_somatorio, 5), round(volume_esfera, 5)

num = int(input('Digite o número de termos: '))
r = int(input('Digite o raio da esfera: '))
pi, vol = realizaCalculos(num, r)
print(f'pi = {pi:.5f}.')
print(f'Volume da esfera = {vol:.5f}.')
