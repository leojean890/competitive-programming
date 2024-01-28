
from collections import deque

lines = []
q = deque()

for i in range(41):
    line = input()
    lines.append(line)
    if "S" in line:
        start = (i, line.index('S'), 0)
        q.appendleft(start)
        visited = {start}

while q:
    y, x, depth = q.pop()

    M = chr(ord(lines[y][x])+1)
    if lines[y][x] == "S":
        M = "a"
    for a,b in ( (y+1, x), (y-1, x), (y, x+1), (y, x-1) ):
        if 0 <= b < 81 and 0 <= a < 41 and lines[a][b] == "E":
            print(depth+1)
            exit()
        if 0 <= b < 81 and 0 <= a < 41 and (a,b) not in visited and 'a' <= lines[a][b] <= M:
            q.appendleft((a,b, depth+1))
            visited.add((a,b))


