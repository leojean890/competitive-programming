from functools import lru_cache
from time import process_time

start_time = process_time()
stones = [i for i in input().split()]
MAX = 75


@lru_cache(None)
def dfs(stone, depth):
    if depth == MAX:
        return 1
    if len(stone) % 2 == 0:
        counter = 0
        for nstone in (stone[:len(stone) // 2], stone[len(stone) // 2:]):
            while nstone[0] == "0" and len(nstone) > 1:
                nstone = nstone[1:]
            counter += dfs(nstone,depth+1)
        return counter
    elif stone == "0":
        return dfs("1",depth+1)
    else:
        return dfs(str(int(stone)*2024), depth + 1)

print(sum([dfs(stone,0) for stone in stones]), process_time() - start_time)  # 261952051690787 0.25
