def main():
    L = float(input('Forneça o comprimento do fio: '))
    P = float(input('Forneça a força peso: '))
    m = float(input('Forneça a massa: '))
    g = P / m
    T = 2 * 3.14 * (L / g) ** 0.5
    print(f'A aceleração da gravidade é {g:.3f}')
    print(f'O período do pêndulo é {T:.3f}')

if __name__ == '__main__':
    main()