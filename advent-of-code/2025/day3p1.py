
counter = 0
N = 100
#input()
for i in range(200):
    line = input()
    M = 0
    for j in range(N-1):
        for k in range(j+1,N):
            candidate = int(line[j])*10+int(line[k])
            if candidate > M:
                M = candidate
    counter+=M
    print(M)

print(counter) # 43952536386
