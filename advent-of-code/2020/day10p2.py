from functools import lru_cache

N = 106#31
@lru_cache(None)
def dfs(current, depth):
    if depth == N+1:
        return 1 if current == voltages[N] else 0

    m = dfs(current, depth+1) if depth != 0 else 0
    if voltages[depth] - current < 4:
        m += dfs(voltages[depth], depth+1)
    return m


voltages = [0]
for i in range(N):
    current = int(input())
    voltages.append(current)

voltages.sort()

print(dfs(0,0)) #96717311574016
