# aller au centre ajoute un niveau
# aller au bord enleve un niveau
# revenir au niveau 0 pour ZZ
# parfois plusieurs options possibles depuis un node mais pas besoin de prioriser via astar
# même pas besoin de telescoper pour chaque voisin (nb de moves et case resultante comme dans le 18) pour accélérer
# car peu de states visités (grâce au hash)

from collections import deque

H = 109
W = 109

paths = set()
tp = {}
lines = []
MX = MY = 0
mX = mY = 1000

for i in range(H):
    line = input()
    lines.append(line)
    for j in range(len(line)):
        if line[j] == ".":
            paths.add((i,j))
            if j < mX:
                mX = j
            if j > MX:
                MX = j
            if i < mY:
                mY = i
            if i > MY:
                MY = i
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
                pairs[a] = (c,1) if a[0] not in (mY,MY) and a[1] not in (mX,MX) else (c,-1)
                pairs[c] = (a,1) if c[0] not in (mY,MY) and c[1] not in (mX,MX) else (a,-1)
                break

(a,b) = start
q = deque()
q.appendleft((a,b,0,0,[(a,b,0)]))
visited = {(a,b)}

while q:
    (y,x,depth,level,path) = q.pop()

    for (a,b) in ((y-1,x),(y+1,x),(y,x+1),(y,x-1)):
        if (a,b,level) not in visited:
            visited.add((a,b,level))
            if (a,b) in paths:
                q.appendleft((a,b,depth+1,level,path+[(a,b,level)]))
            elif (a,b) in pairs:
                ((u,v),levelDelta) = pairs[(a,b)]
                if level+levelDelta >= 0:
                    q.appendleft((u,v,depth+2,level+levelDelta,path+[(a,b,level)]))
            elif ((a,b),level) == (end,0):
                print(depth+1,path) # 5208
                exit()
