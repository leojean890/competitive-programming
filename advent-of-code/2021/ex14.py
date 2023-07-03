
# des qu'on rencontre une paire, on mémoise ce que ça donne au bout de N tours
# ainsi, au lieu de recalculer la même chose en rencontrant encore la même paire, on applique le résultat de la mémo précédente

# ou encore plus rapide, on mémorise uniquement les compteurs de chaque lettre et on les ressort
from functools import lru_cache
import sys
from collections import defaultdict

@lru_cache(None)
def dfs(current, remaining):
    global dp
    if remaining == 0:
        new = defaultdict(int)
        return new

    new = defaultdict(int)
    for i in range(len(current)-1):
        processed = current[i:i+2]
        if True:
            inserted = rules[processed]
            new[inserted] += 1

            found = dfs(current[i] + inserted, remaining-1)
            #print(found, processed, remaining)
            for elt, counter in found.items():
                new[elt] += counter
            #print("b", found)

            # if (inserted + current[i+1], remaining-1) in dp:
            #found = dp[ (inserted + current[i+1], remaining-1)]
            #else:

            found = dfs(inserted + current[i+1], remaining-1)
            for elt, counter in found.items():
                new[elt] += counter
            #print("c", found)

    #new += current[len(current)-1]

    if remaining == N:
        for a in current:
            new[a] += 1

    #dp[(current, remaining)] = new
    return new


sys.setrecursionlimit(10000000)
current = input()
input()
rules = {}

N = 40

for i in range(100):# 16
    pair, res = input().split(" -> ")
    rules[pair] = res

sortedCounters = dfs(current, N)

sortedCounters = list({a:b for a,b in sorted(sortedCounters.items(), key = lambda x:x[1])}.values())

print(sortedCounters)# NN CC BB H

print(sortedCounters[-1]-sortedCounters[0])#4244 4807056953866

