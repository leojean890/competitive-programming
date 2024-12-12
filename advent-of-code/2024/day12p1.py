from collections import deque
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
            while q:
                (y,x) = q.pop()
                area += 1

                for (r,c) in ((y+1,x),(y-1,x),(y,x-1),(y,x+1)):
                    if not 0 <= r < N or not 0 <= c < N or lines[r][c] != lines[i][j]:
                        perimeter += 1
                    elif (r,c) not in visited:
                        q.appendleft((r, c))
                        visited.add((r, c))
            score += area*perimeter

print(score, process_time() - start_time)  # 1473620 0.07
