
counter = 0
N = 100
for i in range(200):
    line = input()
    M = 0
    bestPerSize = {0:""}
    print(line)
    for j in range(N):
        candidate = line[j]
        for k in reversed(bestPerSize.copy().keys()):
            v = bestPerSize[k]
            if k > 0 and candidate > v[-1]:
                bestPerSize[k] = v[:-1] + candidate
            if k > 1 and bestPerSize[k-1] + candidate > v:
                bestPerSize[k] = bestPerSize[k-1] + candidate
            if k < 12 and k+1 not in bestPerSize:
                bestPerSize[k+1] = v + candidate

    M = bestPerSize[12]
    counter+=int(M)
    print(M)

print(counter) # 169685670469164
