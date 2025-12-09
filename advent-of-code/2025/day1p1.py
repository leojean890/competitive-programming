from collections import defaultdict

counters = defaultdict(int)
pos = 50
for i in range(4333):
    ss = input()
    sense = ss[0]
    nb = int(ss[1:])

    pos = (pos+nb if sense == "R" else pos -nb)%100
    counters[pos]+=1

print(counters[0]) # 1048
