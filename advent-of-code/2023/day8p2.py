from collections import defaultdict

mp = {}
actions = input()
input()
starting = []
ending = set()
for i in range(714):
    entree, sortie = input().split(" = (")
    g, d = sortie.split(", ")
    d = d[:-1]
    mp[entree] = {"L":g,"R":d}
    if entree[-1] == "A":
        starting.append(entree)
    if entree[-1] == "Z":
        ending.add(entree)

indexes = defaultdict(list)
for entree in starting:
    courant = entree
    index = 0
    nbActions = 0
    visited = set()
    while (courant, index) not in visited:
        visited.add((courant, index))
        if courant in ending:
            indexes[entree].append(nbActions)
        courant = mp[courant][actions[index]]

        index = (index+1)%len(actions)
        nbActions += 1

def ppcm(a,b):
    p=a*b
    while(a!=b):
        if (a<b): b-=a
        else: a-=b
    return p/a

#print(indexes)
# defaultdict(<class 'list'>, {'RMA': [21883], 'NXA': [19667], 'GDA': [14681], 'PLA': [16897], 'QLA': [13019], 'AAA': [11911]})

# 2 trucs bizarres :

# 1 dans le statement, ce n'est pas précisé un élément par liste 

# 2 ça fonctionne alors que je ne prends pas en compte la taille des cycles, mais j'ai considéré un TP entre le Z et le A ..

print(ppcm(ppcm(ppcm(ppcm(ppcm(21883, 19667),14681),16897),13019),11911)) # 10151663816849

result = 1

for elt in indexes.values():
    result = ppcm(result, elt[0])

print(result) # 10151663816849
