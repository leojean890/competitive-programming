from collections import defaultdict, deque

neighs = defaultdict(list)
for i in range(1069):
    a,b = input().split(")")
    neighs[a].append(b)
    neighs[b].append(a)

q = deque()
q.appendleft(("YOU",0))
visited = {"YOU"}
while q:
    (curr, depth) = q.pop()
    if curr == "SAN":
        print(depth-2) # 367
        exit()

    for neigh in neighs[curr]:
        if neigh not in visited:
            visited.add(neigh)
            q.appendleft((neigh, depth+1))

