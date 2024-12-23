from collections import defaultdict
from time import process_time

start_time = process_time()
N = 3380
connexions = defaultdict(list)
for t in range(N):
    a,b = list(input().split("-"))
    connexions[a].append(b)
    connexions[b].append(a)

triples = []
for a in connexions:
    for i in range(len(connexions[a])-1):
        b = connexions[a][i]
        for j in range(i+1,len(connexions[a])):
            c = connexions[a][j]
            if c in connexions[b]:
                triples.append((a,b,c))

seen= set()
for triple in triples:
    tpl = tuple(sorted(triple))
    if tpl not in seen:
        seen.add(tpl)

counter = 0
for elt in seen:
    if any("t" == tp[0] for tp in elt):
        counter += 1
print(counter,process_time()-start_time) # 1599 0.09375
