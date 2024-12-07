import sys
from collections import deque
from time import process_time

start_time = process_time()
N = 850
counter = 0
sys.setrecursionlimit(10000000)


def dfs(depth, operation):
    if depth == MAX:
        return operation == result

    nops = operation*ops[depth+1]
    if dfs(depth+1,nops):return True
    nops = operation+ops[depth+1]
    if dfs(depth+1,nops):return True
    nops = int(str(operation)+str(ops[depth+1]))
    if dfs(depth+1,nops):return True


for i in range(N):
    result, ops = input().split(":")
    result = int(result)
    ops = [int(j) for j in ops.split()]
    MAX = len(ops) - 1
    q = deque()
    q.appendleft((0,[]))

    if dfs(0,ops[0]):
        counter += result
    print(i,counter)


print(counter, process_time() - start_time) # 116094961956019 12.4375

