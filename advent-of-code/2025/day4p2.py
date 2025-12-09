
counter = 0
N = 137
lines = []
for i in range(N):
    lines.append(list(input()))

intermediateCounter = 1
while intermediateCounter > 0:
    intermediateCounter = 0
    for i in range(N):
        for j in range(N):
            if lines[i][j] == "@":
                nbNeigh = 0
                for (a,b) in ((i+1,j),(i-1,j),(i,j+1),(i,j-1),(i-1,j-1),(i-1,j+1),(i+1,j-1),(i+1,j+1)):
                    if 0 <= a < N and 0 <= b < N and lines[a][b] == "@":
                        nbNeigh += 1
                if nbNeigh < 4:
                    counter += 1
                    intermediateCounter += 1
                    lines[i][j] = 1


print(counter) # 8899
