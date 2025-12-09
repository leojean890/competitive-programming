
counter = 0
N = 4 # 3
lines = []
for i in range(N):
    lines.append(input().split())
print(lines)
operations = input().split()

for i in range(len(operations)):
    current = operations[i].join([lines[j][i] for j in range(N)])
    counter += eval(current)
    print(current)

print(counter) # 6605396225322
