
total = 0

for i in range(200):#200 3
    seq = [int(i) for i in input().split()]
    allSeq = [seq]
    while not all([j == 0 for j in seq]):
        seq = [seq[k+1]-seq[k] for k in range(len(seq)-1)]
        allSeq.append(seq)

    for j in reversed(range(len(allSeq)-1)):
        allSeq[j].append(allSeq[j][-1]+allSeq[j+1][-1])

    total += allSeq[0][-1]

print(total) # 1938731307
