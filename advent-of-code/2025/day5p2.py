
counter = 0
N = 187
M = 1000
intervals = []
for i in range(N):
    intervals.append([int(j) for j in input().split("-")])

newintervals = []
intervals.sort()
for i in range(N):
    print(intervals[i])
    start,end = intervals[i]

    if len(newintervals) > 0 and start <= newintervals[-1][1]:
        if end > newintervals[-1][1]:
            newintervals[-1][1] = end
    else:
        newintervals.append(intervals[i])

for (a,b) in newintervals:
    counter += (b-a+1)
print(counter) # 352716206375547
