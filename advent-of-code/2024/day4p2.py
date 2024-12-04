import re

N = 140
lines = []
for i in range(N):
    lines.append(input())

counter = 0
for i in range(N):
    for j in range(N):
        if 0 < i < N-1 and 0 < j < N-1 and lines[i][j] == "A":
            if lines[i-1][j+1] == "M" == lines[i-1][j-1] and lines[i+1][j+1] == "S" == lines[i+1][j-1]:
                counter += 1
            elif lines[i-1][j+1] == "S" == lines[i-1][j-1] and lines[i+1][j+1] == "M" == lines[i+1][j-1]:
                counter += 1
            elif lines[i-1][j+1] == "M" == lines[i+1][j+1] and lines[i+1][j-1] == "S" == lines[i-1][j-1]:
                counter += 1
            elif lines[i-1][j+1] == "S" == lines[i+1][j+1] and lines[i+1][j-1] == "M" == lines[i-1][j-1]:

                counter += 1

print(counter) # 1910
