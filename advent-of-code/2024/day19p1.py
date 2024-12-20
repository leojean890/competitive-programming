from time import process_time

start_time = process_time()
towels = input().split(", ")
input()
N = 400
counter = 0


def dfs(line):
    if not line:return True
    if line in visited: return
    visited.add(line)
    for towel in towels:
        n = len(towel)
        if towel == line[:n]:
            if dfs(line[n:]):return True


for i in range(N):
    line = input()
    visited = set()
    counter += 1 if dfs(line) else 0

print(process_time() - start_time, counter) # 0.375 338
