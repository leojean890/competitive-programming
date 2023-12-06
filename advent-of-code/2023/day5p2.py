
import sys

def dfs(left, right, depth):
    if depth == maxDepth:
        return left

    M = sys.maxsize
    intervals = []
    for currList in maps[depth]:
        to, frm, lgth = currList

        nleft = max(left, frm)
        nright = min(right, frm+lgth)
        if nleft < nright:
            M = min(M, dfs(nleft + to - frm, nright + to - frm, depth+1))
            intervals.append((nleft,nright))

    intervals.sort()
    current = left
    for (nleft, nright) in intervals:
        if current <= nleft-1:
            M = min(M, dfs(current, nleft-1, depth+1))
        current = nright + 1

    if current <= right:
        M = min(M, dfs(current, right, depth+1))

    return M


lines = []
for i in range(245):
    lines.append(input())

seeds = [int(i) for i in lines[0].split()[1:]]
maps = []
currMap = []
current = 3

while current < len(lines):
    while current < len(lines) and lines[current]:
        currMap.append([int(i) for i in lines[current].split()])
        current += 1
    current += 2
    maps.append(currMap)
    currMap = []

M = sys.maxsize
index = 0
maxDepth = len(maps)
while index < len(seeds):
    seed = seeds[index]
    L = seeds[index+1]
    index += 2
    M = min(dfs(seed, seed+L, 0), M)
print(M) # 47909639
