
counter = 0
N = 187
M = 1000
intervals = []
for i in range(N):
    intervals.append([int(j) for j in input().split("-")])

input()
for j in range(M):
    elt = int(input())
    counter += 1 if any([elt in range(a,b+1) for (a,b) in intervals]) else 0

print(counter) # 694
