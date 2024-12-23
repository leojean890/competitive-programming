from collections import defaultdict
from time import process_time

start_time = process_time()
N = 2244
allDeltas4 = defaultdict(int)
for t in range(N):
    encountered = set()
    nb = int(input())
    ends = []
    deltas = []
    for i in range(2000):
        nb1 = nb*64
        nb = (nb ^ nb1)%16777216
        nb1 = nb//32
        nb = (nb ^ nb1)%16777216
        nb1 = nb*2048
        nb = (nb ^ nb1)%16777216
        ends.append(int(str(nb)[-1]))
        if i > 0:
            deltas.append(ends[-1]-ends[-2])
            if i > 3:
                item = tuple(deltas[-4:])
                if item not in encountered:
                    encountered.add(item)
                    allDeltas4[item] += ends[-1]
print(process_time()-start_time, list({a:b for a,b in sorted(allDeltas4.items(), key=lambda x:x[1])}.items())[-1]) #13.0, ((-1, 0, -1, 2), 2089)
