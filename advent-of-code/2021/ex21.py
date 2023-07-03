
from functools import lru_cache


@lru_cache(None)
def dfs(score0, score1, pos0, pos1, turn):
    if score0 >= 21:
        return 1, 0

    if score1 >= 21:
        return 0, 1

    r0, r1 = 0,0
    if (turn // 3) % 2:
        for i in range(1,4):
            pos = (pos1 + i)%10
            a, b = dfs(score0, score1+pos+1 if (turn % 3) == 2 else score1, pos0, pos, turn+1)
            r0 += a
            r1 += b
    else:
        for i in range(1,4):
            pos = (pos0 + i)%10
            a, b = dfs(score0+pos+1 if (turn % 3) == 2 else score0, score1, pos, pos1, turn+1)
            r0 += a
            r1 += b

    return r0, r1

r0,r1=dfs(0, 0, 4, 8, 0) # 430229563871565 # 3,7

print(max(r0, r1))
print(min(r0, r1))
