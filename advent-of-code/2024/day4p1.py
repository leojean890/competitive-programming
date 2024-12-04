import re

TARGET = "XMAS"
N = 140
lines = []
for i in range(N):
    lines.append(input())

counter = 0
for i in range(N):
    for j in range(N):
        for (dy,dx) in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)):
            for a in range(4):
                if not 0 <= i+a*dy < N or not 0 <= j+a*dx < N or lines[i+a*dy][j+a*dx] != TARGET[a]:
                    break
            else:
                counter += 1

print(counter) # 2560
