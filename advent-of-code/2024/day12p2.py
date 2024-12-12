from collections import deque, defaultdict
from time import process_time

start_time = process_time()
lines = []
N = 140

for j in range(N):
    lines.append(input())

score = 0
visited = set()
for i in range(N):
    for j in range(N):
        if (i,j) not in visited:
            q = deque()
            area = 0
            perimeter = 0
            q.appendleft((i,j))
            visited.add((i,j))
            edges = defaultdict(list)
            while q:
                (y,x) = q.pop()
                area += 1
                for (r,c) in ((y+1,x),(y-1,x),(y,x-1),(y,x+1)):
                    if not 0 <= r < N or not 0 <= c < N or lines[r][c] != lines[i][j]:
                        edges[(r-y,c-x)].append((r,c))
                    elif (r,c) not in visited:
                        q.appendleft((r, c))
                        visited.add((r, c))

            for (a,b) in edges.items():
                perimeter += len(b)
                for rr in range(len(b)-1):
                    (r,c) = b[rr]
                    for rr1 in range(rr+1,len(b)):
                        (y,x) = b[rr1]
                        if abs(r-y)+abs(c-x) == 1:
                            perimeter -= 1

            score += area*perimeter

print(score, process_time() - start_time)  # 902620 0.20
