from collections import deque

H = 109
W = 109

paths = set()
tp = {}
lines = []

for i in range(H):
    line = input()
    lines.append(line)
    for j in range(len(line)):
        if line[j] == ".":
            paths.add((i,j))
        elif line[j].isupper():
            print(i,j)
            if j > 0 and line[j-1] == ".":
                tp[(i,j-1)] = line[j]+line[j+1]
            elif i > 0 and j < len(lines[i-1]) and lines[i-1][j] == ".":
                tp[(i-1,j)] = ((i,j),(i+1,j))
            elif j < len(line)-1 and line[j+1] == ".":
                tp[(i,j+1)] = line[j-1]+line[j]
            elif i > 0 and j < len(lines[i-1]) and lines[i-1][j].isupper() and not (i-2,j) in paths:
                tp[(i+1,j)] = lines[i-1][j]+line[j]

for a,b in tp.items():
    if type(b) == tuple:
        (u,v) = b
        tp[a] = lines[u[0]][u[1]] + lines[v[0]][v[1]]
    paths.remove(a)

pairs = {}

for a,b in tp.items():
    if b == "AA":
        start = a
    if b == "ZZ":
        end = a
    if a not in pairs:
        for c,d in tp.items():
            if d==b and c!=a:
                pairs[a] = c
                pairs[c] = a
                break

(a,b) = start
q = deque()
q.appendleft((a,b,0))
visited = {(a,b)}

while q:
    (y,x,depth) = q.pop()

    for (a,b) in ((y-1,x),(y+1,x),(y,x+1),(y,x-1)):
        if (a,b) not in visited:
            visited.add((a,b))
            if (a,b) in paths:
                q.appendleft((a,b,depth+1))
            elif (a,b) in pairs:
                (u,v) = pairs[(a,b)]
                q.appendleft((u,v,depth+2))
            elif (a,b) == end:
                print(depth+1) # 442
                exit()
