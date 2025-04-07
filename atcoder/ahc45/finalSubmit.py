import math
import random
import time
from collections import defaultdict
from itertools import combinations


def query(c):
    print("?", len(c), *c, flush=True)
    return [tuple(map(int, input().split())) for _ in range(len(c) - 1)]


def answer(groups, edges):
    print("!")
    for i in range(len(groups)):
        print(*groups[i])
        for e in edges[i]:
            print(*e)


N, M, Q, L, W = map(int, input().split())
start_time = time.process_time()
G = list(map(int, input().split()))
lx, rx, ly, ry = [], [], [], []

mX = 10000
mY = 10000
MX = 0
MY = 0

for _ in range(N):
    a, b, c, d = map(int, input().split())
    lx.append(a)
    rx.append(b)
    ly.append(c)
    ry.append(d)
    MX = max(MX, (a+b)//2)
    MY = max(MY, (c+d)//2)
    mX = min(mX, (a+b)//2)
    mY = min(mY, (c+d)//2)

x = [(l + r) // 2 for l, r in zip(lx, rx)]
y = [(l + r) // 2 for l, r in zip(ly, ry)]

cities = list(range(N))

# GLOBAL K-MEANS

nbGrpsWithMoreThan = [sum([1 for g in G if g >= i]) for i in range(1+N)]
centroids = [(random.randint(mX, MX), random.randint(mY, MY)) for i in range(M)]
while time.process_time() - start_time < 1:
    citiesPerCluster = defaultdict(list)
    previousBest = -1
    counterNok = defaultdict(set)
    for city in range(N):
        maxDist = 20000
        best = 0

        for cluster in range(M):
            if city == 0:
                for cluster1 in range(M):
                    if len(citiesPerCluster[cluster1]) > len(citiesPerCluster[cluster]):
                        counterNok[cluster].add(cluster1)
            else:
                if previousBest not in counterNok[cluster] and len(citiesPerCluster[previousBest]) > len(citiesPerCluster[cluster]):
                    counterNok[cluster].add(previousBest)
                if previousBest == cluster:
                    for cluster1 in range(M):
                        if len(citiesPerCluster[cluster1]) <= len(citiesPerCluster[cluster]) and cluster1 in counterNok[cluster]:
                            counterNok[cluster].remove(cluster1)
            counter = len(counterNok[cluster])
            if counter > nbGrpsWithMoreThan[len(citiesPerCluster[cluster])+1]: exit()
            if counter < nbGrpsWithMoreThan[len(citiesPerCluster[cluster])+1]:
                dist = math.dist(centroids[cluster],(x[city],y[city]))
                if dist < maxDist:
                    maxDist = dist
                    best = cluster
        citiesPerCluster[best].append(city)
        previousBest = best
    for cluster in range(M):
        centroids[cluster] = (sum(x[city] for city in citiesPerCluster[cluster])/len(citiesPerCluster[cluster]), sum(y[city] for city in citiesPerCluster[cluster])/len(citiesPerCluster[cluster]))

groups = {}
ngroups = {}

chosen = set()
for cluster in range(M):
    for i in range(M):
        if i not in chosen and len(citiesPerCluster[cluster]) == G[i]:
            chosen.add(i)
            groups[i] = citiesPerCluster[cluster]
            break
if L > 3:
    edges = []
    for k in range(M):
        edges.append([])
        ngroups[k] = []

        nbClusters = math.ceil(G[k]/(L-1))
        if nbClusters > 1:
            mX = 10000
            mY = 10000
            MX = 0
            MY = 0
            for city in groups[k]:
                a = lx[city]
                b = rx[city]
                c = ly[city]
                d = ry[city]
                MX = max(MX, (a + b) // 2)
                MY = max(MY, (c + d) // 2)
                mX = min(mX, (a + b) // 2)
                mY = min(mY, (c + d) // 2)

            centroids = [(random.randint(mX, MX), random.randint(mY, MY)) for i in range(nbClusters)]
            
            # LOCAL K-MEANS FOR THE CURRENT GROUP

            notPassedHere = True

            while notPassedHere or time.process_time() - start_time < 1 + (k+1)/(1.3*M):
                notPassedHere = False
                citiesPerCluster = defaultdict(list)
                for city in groups[k]:
                    maxDist = 20000
                    best = -1
                    for cluster in range(nbClusters):

                        if len(citiesPerCluster[cluster]) < L-1:
                            dist = math.dist(centroids[cluster], (x[city], y[city]))
                            if dist < maxDist:
                                maxDist = dist
                                best = cluster
                    citiesPerCluster[best].append(city)
                for cluster in range(nbClusters):

                    centroids[cluster] = (sum(x[city] for city in citiesPerCluster[cluster]) / len(citiesPerCluster[cluster]),
                                          sum(y[city] for city in citiesPerCluster[cluster]) / len(citiesPerCluster[cluster]))


            # LINK subgroups 2-PER-2 to greedily link them together

            dists = [(math.dist(centroids[v1], centroids[v2]), v1, v2) for v1, v2 in
                     combinations(range(nbClusters), 2)]
            dists.sort()

            groups[k] = []

            chosen = [0 for i in range(nbClusters)]
            (dist, i, j) = dists[0]
            groups[k].append(citiesPerCluster[i])
            chosen[i] = 1
            lastChosen = i
            groups[k].append(citiesPerCluster[j])
            chosen[j] = 1
            lastChosen = j

            while len(groups[k]) < nbClusters:
                maxDist = 20000
                best = None
                for cluster in range(nbClusters):
                    if chosen[cluster] == 0:
                        d = math.dist(centroids[cluster], centroids[lastChosen])
                        if d < maxDist:
                            maxDist = d
                            best = cluster
                chosen[best] = 1
                groups[k].append(citiesPerCluster[best])
                lastChosen = best

        else:
            groups[k] = [groups[k]]

        for i in range(len(groups[k])):
            ngroups[k].extend(groups[k][i])

            if i < len(groups[k])-1:
                maaxed = 20000
                best = groups[k][i+1][0]
                for j in groups[k][i+1]:
                    if time.process_time() - start_time > 1 + (k + 1) / (1.2 * M):
                        break
                    d = min(math.dist((x[j], y[j]), (x[l], y[l])) for l in groups[k][i])
                    if d < maaxed:
                        maaxed = d
                        best = j

                ret = query(groups[k][i]+[best])
                edges[k].extend(ret)

            elif len(groups[k][i]) > 1:
                ret = query(groups[k][i])
                edges[k].extend(ret)

    answer(ngroups, edges)
else:
    edges = []
    for k in range(M):
        edges.append([])
        i = 0
        while i < G[k] - 1:
            delta = min(G[k] - 1 - i, L - 1)

            if delta > -1:
                ret = query(groups[k][i: i + delta + 1])
                edges[k].extend(ret)
            else:
                edges[k].append(groups[k][i: i + 2])
            i += delta

    answer(groups, edges)
