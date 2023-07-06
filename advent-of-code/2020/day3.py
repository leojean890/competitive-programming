for i in range(H):
    lines.append(input())
m = 1
for dy, dx in ((1,1),(1,3),(1,5),(1,7),(2,1)):
    x, y, counter = 0, 0, 0
    while y < H:
        if lines[y][x%W] == "#":
            counter += 1
        y += dy
        x += dx
    m *= counter

print(m) #244 9406609920
