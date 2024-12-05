from collections import defaultdict

N = 1385
part1 = True
lines = []
before = defaultdict(list)
counter = 0

for i in range(N):
    line = input()
    if not line:
        part1 = False
    elif part1:
        a,b = [int(j) for j in line.split('|')]
        before[b].append(a)
    else:
        line = [int(j) for j in line.split(',')]
        
        v = True
        for k in range(len(line)-1):
            a = line[k]
            if v:
                for j in range(k+1,len(line)):
                    b = line[j]
                    if b in before[a]:
                        v = False
                        break
            else:
                break
        if v:
            counter += line[len(line)//2]
print(counter) # 5275
