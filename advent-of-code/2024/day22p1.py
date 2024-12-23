from time import process_time

start_time = process_time()
N = 2244
counter = 0
for t in range(N):
    nb = int(input())
    for i in range(2000):
        nb1 = nb*64
        nb = (nb ^ nb1)%16777216
        nb1 = nb//32
        nb = (nb ^ nb1)%16777216
        nb1 = nb*2048
        nb = (nb ^ nb1)%16777216
    counter += nb
print(counter) #18525593556
