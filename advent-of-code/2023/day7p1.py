
from collections import defaultdict
from functools import cmp_to_key

cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]


def compare(hand1, hand2):
    for i in range(5):
        if cards.index(hand1[0][i]) > cards.index(hand2[0][i]):
            return 1
        if cards.index(hand1[0][i]) < cards.index(hand2[0][i]):
            return -1
    return 0


def getType(counters):

    if 5 in counters.values():
        return 0
    if 4 in counters.values():
        return 1
    if 3 in counters.values() and 2 in counters.values():
        return 2
    if 3 in counters.values():
        return 3
    if list(counters.values()).count(2) == 2:
        return 4
    if 2 in counters.values():
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
        
    allTypes[getType(counters)].append((hand,score)) 

current = N
total = 0
for i in range(7):
    for (hand, score) in list(sorted(allTypes[i], key=cmp_to_key(compare))):
        total += current * score
        current -= 1

print(total) # 253313241


