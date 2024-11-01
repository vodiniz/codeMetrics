'''input
5
3 1
3 2
3 3
4 0
5 2

'''
import sys
read = lambda: list(map(int,sys.stdin.readline().strip().split()))

# try:
sigma = lambda x:x*(x+1)//2
for _ in range(int(input())):
    n,m = read()
    k = n-m
    total = sigma(n)
    # if m==0 or m==n:
    #     print(total)
    #     continue
    if k>m:
        e,f = divmod(k,m+1)
        total -= (m+1-f)*sigma(e)+f*sigma(e+1)
    else:
        total -= k
    print(total)