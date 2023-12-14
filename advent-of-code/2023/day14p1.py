
N = 100
lines = []

for i in range(N):
    lines.append(list(input()))

for i in range(1, N):
    for j in range(N):
        if lines[i][j] == "O":
            current = i
            while current-1 >= 0 and lines[current-1][j] == ".":
                current -= 1
            lines[i][j] = "."
            lines[current][j] = "O"


total = 0
for i in range(N):
    total += lines[i].count("O") * (N-i)

print(total) # 108813
