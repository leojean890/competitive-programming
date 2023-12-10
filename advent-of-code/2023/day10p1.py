from collections import deque


def validate(y,x,a,b):
    if lines[y][x] == "J":
        if a == y-1 and lines[a][b] in ("|", "7", "F"):
            return True
        if b == x-1 and lines[a][b] in ("-", "L", "F"):
            return True

    if lines[y][x] == "L":
        if a == y-1 and lines[a][b] in ("|", "7", "F"):
            return True
        if b == x+1 and lines[a][b] in ("-", "J", "7"):
            return True

    if lines[y][x] == "7":
        if a == y+1 and lines[a][b] in ("|", "L", "J"):
            return True
        if b == x-1 and lines[a][b] in ("-", "L", "F"):
            return True

    if lines[y][x] == "F":
        if a == y+1 and lines[a][b] in ("|", "L", "J"):
            return True
        if b == x+1 and lines[a][b] in ("-", "J", "7"):
            return True

    if lines[y][x] == "|":
        if a == y+1 and lines[a][b] in ("|", "L", "J"):
            return True
        if a == y-1 and lines[a][b] in ("|", "7", "F"):
            return True

    if lines[y][x] == "-":
        if b == x+1 and lines[a][b] in ("-", "J", "7"):
            return True
        if b == x-1 and lines[a][b] in ("-", "L", "F"):
            return True

    if lines[y][x] == "S":
        if b == x+1 and lines[a][b] in ("-", "J", "7"):
            return True
        if b == x-1 and lines[a][b] in ("-", "L", "F"):
            return True
        if a == y+1 and lines[a][b] in ("|", "L", "J"):
            return True
        if a == y-1 and lines[a][b] in ("|", "7", "F"):
            return True


N = 140
lines = []
for i in range(N):
    line = input()
    lines.append(line)
    for j in range(N):
        if line[j] == "S":
            entrance = (i,j)

q = deque()
q.appendleft((entrance[0], entrance[1], 0))
visited = {entrance}
M = 0
while q:
    (y,x,depth) = q.pop()
    M = max(depth,M)
    for (a,b) in ((y+1,x), (y-1,x),(y,x+1),(y,x-1)):
        if 0 <= a < N and 0 <= b < N and (a,b) not in visited and validate(y,x,a,b):
            q.appendleft((a,b,depth+1))
            visited.add((a,b))

print(M) # 7107
