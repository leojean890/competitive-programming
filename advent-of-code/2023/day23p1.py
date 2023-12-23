from collections import deque

N = 141
lines = []
start = (0,1)
end = (N-1,N-2)

for i in range(N):
    lines.append(input())

q = deque()
q.appendleft((0,1,0,{(0,1)}))
M = 0
arrows = {"<":(0,-1),"^":(-1,0),"v":(1, 0),">":(0,1)}

while q:
    y, x, depth, path = q.pop()
    if (y,x) == end:
        if depth > M:
            M = depth
        continue

    if lines[y][x] in arrows:
        (dy, dx) = arrows[lines[y][x]]
        (a,b) = (y+dy, x+dx)
        if lines[a][b] != "#" and (a,b) not in path:
            q.appendleft((a, b, depth+1, path|{(a,b)}))
    else:
        for (a,b) in ((y+1,x),(y-1,x),(y,x+1),(y,x-1)):
            if lines[a][b] != "#" and (a,b) not in path:
                q.appendleft((a, b, depth+1, path|{(a,b)}))
print(M) # 2094

