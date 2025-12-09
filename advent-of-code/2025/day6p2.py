
counter = 0
N = 4
lines = []
for i in range(N):
    lines.append(input())
print(lines)
operations = input().split()

currIndex = 0
for i in range(len(operations)):
    currLines = []
    while not (currIndex >= len(lines[0]) or all(lines[j][currIndex] == " " for j in range(N))):
        currLines.append("".join([lines[j][currIndex] for j in range(N) if lines[j][currIndex] != " "]))
        currIndex += 1
    currIndex += 1

    current = operations[i].join(currLines)
    counter += eval(current)
    print(current)

print(counter) # 11052310600986
