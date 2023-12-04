from collections import defaultdict

total = 0
N = 208
nbs = defaultdict(int)
for i in range(N):
    nbs[i] += 1
    game = input().split(":")[1].split("|")
    my_cards = game[0].split()
    other_cards = game[1].split()
    score = 0
    j = i+1
    for card in other_cards:
        if card in my_cards:
            nbs[j] += nbs[i]
            j += 1
print(sum(nbs.values())) #5659035
