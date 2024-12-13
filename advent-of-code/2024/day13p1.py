import sys
from collections import defaultdict
from time import process_time

start_time = process_time()
elts = defaultdict(list)
N = 1279
penalties = [3,1]

for j in range(N):
    s = input()
    if j%4 < 2:
        elts[j//4].append([int(a[-2:]) for a in s.split(":")[1].split(",")])
    elif j%4 == 2:
        elts[j//4].append([int(a.split("=")[1]) for a in s.split(":")[1].split(",")])

score = 0


def dfs(currentX, currentY, nb0, nb1):
    if (currentX, currentY, nb0, nb1) in memo:
        return memo[(currentX, currentY, nb0, nb1)]
    if currentX > elt[2][0] or currentY > elt[2][1]:
        memo[(currentX, currentY, nb0, nb1)] = None
        return

    if [currentX, currentY] == elt[2]:
        memo[(currentX, currentY, nb0, nb1)] = 0
        return 0
    if nb0 >= 100 or nb1 >= 100:
        memo[(currentX, currentY, nb0, nb1)] = None
        return None
    MAX = sys.maxsize

    for i in range(2):
        output = dfs(currentX+elt[i][0], currentY+elt[i][1], nb0 + (1 if i == 0 else 0), nb1 + (1 if i == 1 else 0))
        if output is not None:
            penalty = output+penalties[i]
            if penalty < MAX:
                MAX = penalty
    memo[(currentX, currentY, nb0, nb1)] = MAX

    return MAX


for index, elt in elts.items():
    memo = {}
    points = dfs(0, 0, 0, 0)
    if points < sys.maxsize:
        score += points

print(score, process_time() - start_time)  # 39290 4.85
