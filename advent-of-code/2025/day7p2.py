from functools import lru_cache

counter = 0
N = 142#16
splitters = []
for i in range(N):
    line = input()
    for j in range(N-1):
        if line[j] == "S":
            start = (i,j)
        if line[j] == "^":
            splitters.append((i,j))

(i,j) = start

@lru_cache(None)
def dfs(y, x):
    return ((dfs(y + 1, x+1) + dfs(y + 1, x-1)) if (y,x) in splitters else dfs(y + 1, x)) if y < N else 1

print(dfs(i,j)) # 25489586715621
