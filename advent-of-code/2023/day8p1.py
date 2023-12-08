mp = {}
actions = input()
input()
for i in range(714):
    entree, sortie = input().split(" = (")
    g, d = sortie.split(", ")
    d = d[:-1]
    mp[entree] = {"L":g,"R":d}

courant = "AAA"
index = 0
nbActions = 0
while courant != "ZZZ":
    courant = mp[courant][actions[index]]
    index = (index+1)%len(actions)
    nbActions += 1

print(nbActions) # 11911
