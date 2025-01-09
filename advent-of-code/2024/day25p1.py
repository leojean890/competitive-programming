from time import process_time

start_time = process_time()
N = 3999
W = 5
H = 7
keys = []
locks = []
current = []
for t in range(N+1):
    line = input() if t < N else ""
    if not line:
        lines = []
        for j in range(W):
            counter = 0
            for i in range(H):
                if current[i][j] == "#":
                    counter += 1
            lines.append(counter)
        if current[0] == "#####":
            keys.append(lines)
        else:
            locks.append(lines)
        current = []
    else:
        current.append(line)

counter = 0
for key in keys:
    for lock in locks:
        if all(key[i]+lock[i] <= H for i in range(W)):
            counter += 1

print(counter,process_time()-start_time) # 3690 0.109
