import random
from collections import defaultdict

N, D, Q = [int(v) for v in input().split(" ")]
threshold = 4*Q//5

TTT = 28
factor = 20
stats = defaultdict(int)
nVisited = defaultdict(int)
elts = tuple(range(N))
tried = {elts}
for q in range(Q):
    X = len(elts)
    print(X//2, X-X//2, *elts)

    res = input()

    if res == "<":
        for elt in elts[:N//2]:
            stats[elt] -= 1
            nVisited[elt] += 1
        for elt in elts[N//2:]:
            stats[elt] += 1
            nVisited[elt] += 1

    if res == ">":
        for elt in elts[:N//2]:
            stats[elt] += 1
            nVisited[elt] += 1

        for elt in elts[N//2:]:
            stats[elt] -= 1
            nVisited[elt] += 1

    sortedStats = {a:b/nVisited[a] for a,b in sorted(stats.items(), key=lambda x:x[1]/nVisited[x[0]])}

    if q < Q//10:
        currentPackages = {}
        currentPackage = 0

        for (a, b) in sortedStats.items():
            currentPackages[a] = currentPackage
            currentPackage = (currentPackage + 1) % 2

    else:
        moy = 0
        for (a, b) in sortedStats.items():
            moy += b
        moy /= N

        if q > 4 * Q // 5:
            factor = 10
        elif q > 2 * Q // 3:
            factor = 20
        else:
            factor = 100
            for x in range(3, 10):
                if q > Q // x:
                    factor = 10*x
                    break

        gaps = []
        for i in range(N):
            gaps.append(abs(moy - sortedStats[i]))
        gaps.sort()
        med = gaps[N//2]

        currentPackages = {}
        currentPackage = 0

        for (a, b) in sortedStats.items():
            if abs(moy - b) <= factor*med: # utiliser la médiane
                currentPackages[a] = currentPackage
                currentPackage = (currentPackage + 1) % 2

    elts = [a for a in currentPackages if currentPackages[a] == 0] + [a for a in currentPackages if currentPackages[a] == 1]
    telts = tuple(elts)

    if telts in tried:
        random.shuffle(elts)
        telts = tuple(elts)

    tried.add(telts)


finalPackages = {}
currentPackage = 0
sens = 0
lll = list(sortedStats.keys())
ll = len(lll)
for i in range(ll//2):
    a = lll[i]
    b = lll[ll-1-i]
    finalPackages[a] = currentPackage
    finalPackages[b] = currentPackage
    if sens == 0:
        currentPackage = currentPackage+1
        if currentPackage == D:
            sens = 1
            currentPackage = D-1
    else:
        currentPackage = currentPackage-1
        if currentPackage == -1:
            sens = 0
            currentPackage = 0
if ll%2:
    finalPackages[lll[ll//2]] = currentPackage
print(*[finalPackages[i] for i in range(N)])

