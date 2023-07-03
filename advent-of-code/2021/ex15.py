import sys
from functools import lru_cache
sys.setrecursionlimit(100000000)
W = 100
H = 100
lines = []



def ggg(k, j):
    v = int(k)+j
    if v > 9:
        return v%10+1
    else:
        return v

for i in range(H):
    line = [int(j) for j in input()]
    for j in range(1,5):
        line.extend([ggg(k,j) for k in line[:W]])
    lines.append(line)
    #print(line)


for j in range(1,5):
    for i in range(H):
        lines.append([ggg(k,j) for k in lines[i]])
        #print(lines[-1])

visited = set()
@lru_cache(None)
def dfs(i, j):
    global visited

    if (i, j) == (5*H-1, 5*W-1):
        return lines[i][j]

    m = sys.maxsize
    for (a, b) in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        #for (a, b) in ((i + 1, j), (i, j + 1)):
        if (a, b) not in visited and 0 <= a < 5*H and 0 <= b < 5*W:
            visited.add((a,b))
            res = dfs(a,b)
            if res < m:
                m = res

    return m + lines[i][j]

print(dfs(0,0)-lines[0][0]) #2998
