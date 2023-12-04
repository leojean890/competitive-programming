
total = 0
N = 208

for i in range(N):
    game = input().split(":")[1].split("|")
    my_cards = game[0].split()
    other_cards = game[1].split()
    score = 0
    for card in other_cards:
        if card in my_cards:
            if score:
                score *= 2
            else:
                score = 1
    total += score
print(total) #24160


