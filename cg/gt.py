
lines = []
width, height = [int(i) for i in input().split()]
count = int(input())

for i in range(height):
    raster = input()
    lines.append(list(raster))

for i in range(count%8):

    cols = []
    for line in lines:
        cols.append(line)

    lines = []
    for col in cols:
        lines.append((len(col)-col.count('#'))*['.'] + col.count('#')*['#'])

    cols = list(map(list, zip(*lines)))
    
    lines = []
    for col in cols:
        lines.append((len(col)-col.count('#'))*['.'] + col.count('#')*['#'])

for i in range(len(lines)):
    print(*lines[i],sep="")
