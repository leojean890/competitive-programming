from collections import deque

counter = 0
N = 142
splitters = []
for i in range(N):
    line = input()
    for j in range(N-1):
        if line[j] == "S":
            start = (i,j)
        if line[j] == "^":
            splitters.append((i,j))

q = deque()
q.appendleft(start)
visited = set()

while q:
    current = q.pop()
    (y,x) = current
    if current not in visited and y < N:
        visited.add(current)
        if current in splitters:
            q.appendleft((y+1,x-1))
            q.appendleft((y+1,x+1))
            counter += 1
        else:
            q.appendleft((y + 1, x))

print(counter) # 11052310600986
