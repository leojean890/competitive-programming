from collections import deque, defaultdict

score = 0
allCubes = set()
while 1:
    try:
        curr = tuple([int(i) for i in input().split(",")])
        allCubes.add(curr)

    except Exception as ex:
        break

print(allCubes)

counters = defaultdict(int)
visited = set()

for elt in allCubes:
    if elt not in visited:
        q = deque()
        q.appendleft(elt)
        visited.add(elt)

        while q:
            (x,y,z) = q.pop()

            for (a,b,c) in ((x+1,y,z), (x-1,y,z), (x,y+1,z), (x,y-1,z), (x,y,z+1), (x,y,z-1)):
                if (a,b,c) in allCubes:
                    if (a,b,c) not in visited:
                        q.appendleft((a,b,c))
                        visited.add((a, b, c))
                else:
                    counters[(a,b,c)] += 1

print(counters)
print(sum(counters.values()))

sortedCounters = [a for a,b in sorted(counters.items(), key = lambda x:x[0])]
sortedCountersSet = set(sortedCounters)
print(sortedCounters)

MX = max([counter[0] for counter in sortedCounters]) + 3
mX = min([counter[0] for counter in sortedCounters]) - 3
MY = max([counter[1] for counter in sortedCounters]) + 3
mY = min([counter[1] for counter in sortedCounters]) - 3
MZ = max([counter[2] for counter in sortedCounters]) + 3
mZ = min([counter[2] for counter in sortedCounters]) - 3

counter = 0

visited = set()
elt = sortedCounters[0]
q = deque()
q.appendleft(elt)
visited.add(elt)
counter += counters[elt]

while q:
    (x,y,z) = q.pop()

    for (a,b,c) in ((x+1,y,z), (x-1,y,z), (x,y+1,z), (x,y-1,z), (x,y,z+1), (x,y,z-1)):
        if (a,b,c) in sortedCounters:
            if (a,b,c) not in visited:
                q.appendleft((a,b,c))
                visited.add((a, b, c))
                counter += counters[(a,b,c)]
        elif mX < a < MX and mY < b < MY and mZ < c < MZ and (a,b,c) not in visited and (a,b,c) not in allCubes:
            q.appendleft((a, b, c))
            visited.add((a, b, c))

print(counter)
