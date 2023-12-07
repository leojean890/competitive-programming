
from collections import defaultdict
from functools import cmp_to_key

cards = ["A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"]


def compare(hand1, hand2):
    for i in range(5):
        if cards.index(hand1[0][i]) > cards.index(hand2[0][i]):
            return 1
        if cards.index(hand1[0][i]) < cards.index(hand2[0][i]):
            return -1
    return 0


def getType(counters):
    M = max(counters.values())

    if "J" in counters.keys():
        MsansJ = 0 # pas 1 car il y a le cas de JJJJJ
        for (a,b) in counters.items():
            if "J" != a and b > MsansJ:
                MsansJ = b
        MsansJ += counters["J"]
        M = max(MsansJ, M)

    if 5 == M:
        return 0
    elif 4 == M:
        return 1
    elif 3 == M and (list(counters.values()).count(2) == 2 or (3 in counters.values() and 2 in counters.values())):
        return 2
    elif 3 == M:
        return 3
    elif list(counters.values()).count(2) == 2:
        return 4
    elif 2 == M:
        return 5
    return 6


N = 1000
allTypes = defaultdict(list)


for i in range(N):
    hand, score = input().split()
    score = int(score)

    counters = defaultdict(int)

    for char in hand:
        counters[char] += 1

    type1 = getType(counters)
    allTypes[type1].append((hand, score))

current = N
total = 0
for i in range(7):
    for (hand, score) in list(sorted(allTypes[i], key=cmp_to_key(compare))):
        total += current * score
        current -= 1

print(total) # 253362743
