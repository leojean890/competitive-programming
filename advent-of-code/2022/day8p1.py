N = 99
lines = []
visible = []

for i in range(N):
    lines.append([int(j) for j in input()])
    visible.append([False]*N)

for i in range(N):
    m = -1
    for j in range(N):
        if lines[i][j] > m:
            visible[i][j] = True
            m = lines[i][j]

    m = -1
    for j in reversed(range(N)):
        if lines[i][j] > m:
            visible[i][j] = True
            m = lines[i][j]

    m = -1
    for j in range(N):
        if lines[j][i] > m:
            visible[j][i] = True
            m = lines[j][i]


    m = -1
    for j in reversed(range(N)):
        if lines[j][i] > m:
            visible[j][i] = True
            m = lines[j][i]



total = 0
for v in visible:
    total += v.count(True)
print(total)
