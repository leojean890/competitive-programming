from collections import defaultdict, deque

neighs = defaultdict(list)

for i in range(594):
    father, sons = input().split(" contain")
    father = father.replace("bags","bag").replace(".","")

    for son in sons.split(","):
        if son[1].isdigit():
            child = son[3:].replace("bags","bag").replace(".","")
            neighs[father].append((int(son[1]), child))

q = deque()
q.appendleft((1, "shiny gold bag"))
nbBags = 0
while q:
    nb, current = q.pop()
    if current in neighs:
        for ctr, neigh in neighs[current]:
            cc = nb*ctr
            nbBags += cc
            q.appendleft((cc, neigh))

print(nbBags) #82930
