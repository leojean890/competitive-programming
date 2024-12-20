from functools import lru_cache
from time import process_time

start_time = process_time()
towels = input().split(", ")
input()
N = 400
counter = 0


@lru_cache(None)
def dfs(line):
    if not line:return 1
    m = 0
    for towel in towels:
        n = len(towel)
        if towel == line[:n]:
            m += dfs(line[n:])
    return m


for i in range(N):
    line = input()
    visited = set()
    counter += dfs(line)

print(process_time() - start_time, counter) # 1.5625 841533074412361
