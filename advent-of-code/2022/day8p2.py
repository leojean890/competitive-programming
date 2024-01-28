N = 99
lines = []

for i in range(N):
    lines.append([int(j) for j in input()])

#visible[10][10] = True
#print(visible[8:11])
bM = 0
for i in range(N):
    for j in range(N):
        counter = 0
        m = lines[i][j]
        c = j+1
        while c < N and lines[i][c] < m:
            counter += 1
            c += 1
        if c < N:
            counter += 1

        mult = counter
        counter = 0
        c = j-1
        while c >= 0 and lines[i][c] < m:
            counter += 1
            c -= 1
        if c >= 0:
            counter += 1

        mult *= counter

        counter = 0
        c = i+1
        while c < N and lines[c][j] < m:
            counter += 1
            c += 1
        if c < N:
            counter += 1

        mult *= counter

        counter = 0
        c = i-1
        while c >= 0 and lines[c][j] < m:
            counter += 1
            c -= 1
        if c >= 0:
            counter += 1

        mult *= counter

        if mult > bM:
            bM = mult



print(bM)

