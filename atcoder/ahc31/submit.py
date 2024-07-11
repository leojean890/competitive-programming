
import math

W, D, N = map(int, input().split())
a = []
moyPerArea = [0 for _ in range(N)]
sortedD = []

for d in range(D):
    l = list(map(int, input().split()))
    a.append(l)
    sortedDD = []
    for i in range(N):
        moyPerArea[i] += l[i]
        sortedDD.append((l[i],i))
    sortedD.append(list(sorted(sortedDD)))

maxPerSorted = []
moyOfMoyPerArea = 0
for i in range(N):
    moyPerArea[i] /= D
    moyOfMoyPerArea += moyPerArea[i]
    maxPerSorted.append(max(sortedD[j][i][0] for j in range(D)))

moyOfMoyPerArea /= N

rect = [[] for _ in range(D)]
for d in range(D):
    for k in range(N-1):
        curr = rect[d][-1][2] if rect[d] else 0
        delta = math.ceil(int((W * moyPerArea[k]) / (N * moyOfMoyPerArea)))
        v = math.ceil(max(a[j][k] for j in range(D))/W)

        rect[d].append((curr, 0, curr + max(1,min(delta,v)), W))
    rect[d].append((rect[d][-1][2] if rect[d] else 0, 0, W, W))

for d in range(D):
    for k in range(N):
        i0, j0, i1, j1 = rect[d][k]
        print(i0, j0, i1, j1)
