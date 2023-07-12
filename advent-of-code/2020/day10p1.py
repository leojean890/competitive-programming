from collections import defaultdict

voltages = [0]
for i in range(106):
    current = int(input())
    voltages.append(current)

voltages.sort()
counters = defaultdict(int)
for i in range(106):
    counters[voltages[i+1]-voltages[i]] += 1

print((counters[1])*(counters[3]+1))#+1 car la fin => 2482
