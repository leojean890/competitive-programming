
lines = tuple()
for i in range(5):
    lines += (input(),)

visited = set()

while lines not in visited:
    visited.add(lines)
    nlines = tuple()

    for i in range(5):
        line = ""
        for j in range(5):
            neighs = 0
            if j > 0 and lines[i][j-1] == "#":
                neighs += 1
            if i > 0 and lines[i-1][j] == "#":
                neighs += 1
            if j < 4 and lines[i][j+1] == "#":
                neighs += 1
            if i < 4 and lines[i+1][j] == "#":
                neighs += 1

            if lines[i][j] == "#":
                line += "#" if neighs == 1 else "."
            else:
                line += "#" if neighs in (1,2) else "."
        nlines += (line,)
    lines = nlines


total = 0
power = 0
for i in range(5):
    for j in range(5):
        if lines[i][j] == "#":
            total += 2**power
        power += 1

print(total) # 32505887
