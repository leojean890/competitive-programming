
from collections import defaultdict, deque

neighs = defaultdict(list)

for i in range(594):
    father, sons = input().split(" contain")
    father = father.replace("bags","bag").replace(".","")

    for son in sons.split(","):
        child = son[3:].replace("bags","bag").replace(".","")
        neighs[child].append(father)

q = deque()
q.appendleft("shiny gold bag")
visited = {"shiny gold bag"}
while q:
    current = q.pop()
    if current in neighs:
        #for nb,neigh in neighs[current]:
        for neigh in neighs[current]:
            if neigh not in visited:
                q.appendleft(neigh)
                visited.add(neigh)

print(len(visited)-1) # 238
