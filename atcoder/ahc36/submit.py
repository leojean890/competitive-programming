from collections import defaultdict, deque
from time import process_time

F1 = 90
F2 = 2
F3 = 8


def dist(a, b):
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


N, M, T, L_A, L_B = map(int, input().split())
start_time = process_time()

G = [[] for _ in range(N)]

for _ in range(M):
    u, v = map(int, input().split())
    G[u].append(v)
    G[v].append(u)

t = list(map(int, input().split()))

P = []
for _ in range(N):
    x, y = map(int, input().split())
    P.append((x, y))

A = [0] * L_A
B = [-1] * L_B

pos_from = 0
globalPath = []
encountered = set()
notablePos = set()

for pos_to in t:
    visited = [False] * N
    q = deque()
    q.appendleft((pos_from, -1, []))

    while q:
        (cur, prev, path) = q.pop()
        if cur == pos_to:
            break
        for v in G[cur]:
            if not visited[v]:
                visited[v] = True
                q.appendleft((v, cur, path+[v]))

    for u in path:
        globalPath.append(u)
        if u not in encountered:
            encountered.add(u)
    notablePos.add(len(globalPath)-1)
    pos_from = pos_to

counter = defaultdict(int)
for i in range(len(globalPath)):
    for j in range(i+1,min(i+L_B,len(globalPath))):
        counter[tuple(globalPath[i:j+1])] += 1

sC = {a: b for a, b in sorted(counter.items(), key=lambda x: F1*len(x[0])+F3*x[1], reverse=True)}
sortedC = list(sC.keys())
ctr = {0:L_A}

i = 0
c = 0
TT = 1.7
if L_B < 9 and L_A < 3*N/2:
    TT = 2.0
elif L_B < 14 and L_A < 3*N/2:
    TT = 1.9
elif L_B > 14 and L_A < 3*N/2:
    TT = 1.8
elif L_B < 14 and L_A > 3*N/2:
    TT = 1.8

while i < L_A:
    if process_time() - start_time < TT:

        lst = sortedC[0]
        del sC[lst]

        for elt in lst:
            A[i] = elt
            i += 1
            if i == L_A:
                break
        if i < L_A:
            ctr = defaultdict(int)

            for j in range(i):
                ctr[A[j]] += 1

            ctr[0] = 5

            sC = {a: b for a, b in sorted(sC.items(), key=lambda x: F1 * len(x[0]) + F3*x[1] + 2 * F2 * len(
                [y for y in x[0] if ctr[y] == 0]) + 1.5 * F2 * len([y for y in x[0] if ctr[y] < 2]) + F2 * len(
                [y for y in x[0] if ctr[y] < 3]) + 0.5 * F2 * len([y for y in x[0] if ctr[y] < 4]), reverse=True)}
            sortedC = list(sC.keys())
    else:
        lst = sortedC[c]
        c += 1
        for elt in lst:
            A[i] = elt
            i += 1
            if i == L_A:
                break

c = 1
anyNotInA = True
while anyNotInA:
    anyNotInA = False
    for i in encountered:
        if i not in A:
            A[-c] = i
            c += 1
            anyNotInA = True

print(*A)
for counter in range(len(globalPath)):
    u = globalPath[counter]

    if u not in B:

        didNotChange = True

        if counter not in notablePos and 0 < counter < len(globalPath)-1:
            for neigh in G[globalPath[counter-1]]:
                if neigh in G[globalPath[counter+1]] and neigh in B:
                    u = neigh
                    globalPath[counter] = u
                    didNotChange = False
                    break

        if didNotChange:

            best = 0
            bestD = 0
            for start in range(L_A):
                for end in range(min(L_B-1,L_A-start),min(L_B+1,L_A-start+1)):
                    for startInB in range(L_B-end+1):
                        listToCatch = B[:startInB] + A[start:start+end] + B[startInB+end:]
                        for j in range(L_B):
                            if counter+j == len(globalPath):
                                bestD = j
                                best = (start,end,startInB,listToCatch)
                                break
                            if globalPath[counter+j] not in listToCatch:
                                if j > bestD:
                                    bestD = j
                                    best = (start, end, startInB, listToCatch)
                                break
                        else:
                            bestD = j
                            best = (start, end, startInB, listToCatch)

            (start, end, startInB, listToCatch) = best
            print('s', end, start, startInB)
            B = listToCatch

    print('m', u)
