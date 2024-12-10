from collections import deque
from time import process_time

start_time = process_time()
N = 41
starts = []
lines = []
for i in range(N):
    line = [int(i) for i in input()]
    lines.append(line)
    for j in range(N):
        if line[j] == 0:
            starts.append((i,j))

counter = 0
for (y,x) in starts:
    q = deque()
    q.appendleft((y,x))

    while q:
        (r,c) = q.pop()
        value = lines[r][c]
        for (a,b) in ((r+1,c),(r-1,c),(r,c+1),(r,c-1)):
            if 0 <= a < N and 0 <= b < N and lines[a][b] == value+1:
                q.appendleft((a,b))
                if lines[a][b] == 9:
                    counter += 1

print(counter, process_time() - start_time)  # 1186
