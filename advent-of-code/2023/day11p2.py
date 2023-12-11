
N = 140
factor = 999999
lines = []
doubledX = set()
doubledY = set()
galaxies = []
for i in range(N):
    line = input()
    lines.append(list(line))
    if all(line[j] == "." for j in range(N)):
        doubledY.add(i)

for i in range(N):
    if all(lines[j][i] == "." for j in range(len(lines))):
        doubledX.add(i)

for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == "#":
            galaxies.append((i, j))

s = 0
for i in range(len(galaxies)-1):
    for j in range(i+1,len(galaxies)):
        mX = min(galaxies[i][1], galaxies[j][1])
        MX = max(galaxies[i][1], galaxies[j][1])
        mY = min(galaxies[i][0],galaxies[j][0])
        MY = max(galaxies[i][0],galaxies[j][0])
        for k in range(mX, MX+1):
            if k in doubledX:
                s += factor
        for k in range(mY, MY+1):
            if k in doubledY:
                s += factor
        s += abs(mX-MX) + abs(mY - MY)
        
print(s) # 649862989626

